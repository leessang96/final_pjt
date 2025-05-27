<template>
  <div>
    <div style="display: flex; gap: 0.5rem; align-items: center">
      <h2 @click="loadTerm" style="cursor: pointer">정기예금</h2>
      <button @click="store.fetchAndStoreTermProducts">정기예금 최신화</button>
      <h2>|</h2>
      <h2 @click="loadSaving" style="cursor: pointer">적금</h2>
      <button @click="store.fetchAndStoreSavingProducts">적금 최신화</button>
    </div>

    <div>
      <label>
        금융회사명:
        <input type="text" v-model="filterBank" placeholder="금융회사 명을 적으세요">
      </label>

      <label>
        예치기간:
        <select v-model="filterTerm">
          <option value="">전체</option>
          <option value="1">1개월</option>
          <option value="3">3개월</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
      </label>
    </div>

    <table v-if="paginatedProducts.length" border="1" style="width: 100%">
      <thead>
        <tr>
          <th>공시 제출월</th>
          <th>금융회사 명</th>
          <th>상품 명</th>
          <th @click="sortByTerm('1')" style="cursor: pointer">1개월</th>
          <th @click="sortByTerm('3')" style="cursor: pointer">3개월</th>
          <th @click="sortByTerm('6')" style="cursor: pointer">6개월</th>
          <th @click="sortByTerm('12')" style="cursor: pointer">12개월</th>
          <th @click="sortByTerm('24')" style="cursor: pointer">24개월</th>
          <th @click="sortByTerm('36')" style="cursor: pointer">36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in paginatedProducts" :key="product.fin_prdt_cd + '-' + product.fin_co_no" @click="openProductModal(product)" style="cursor: pointer">
          <td>{{ product.dcls_month }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ getRateByTerm(product, '1') }}</td>
          <td>{{ getRateByTerm(product, '3') }}</td>
          <td>{{ getRateByTerm(product, '6') }}</td>
          <td>{{ getRateByTerm(product, '12') }}</td>
          <td>{{ getRateByTerm(product, '24') }}</td>
          <td>{{ getRateByTerm(product, '36') }}</td>
        </tr>
      </tbody>
    </table>

    <teleport to="body">
      <div v-if="showModal" class="modal">
        <h3>상품 세부 정보</h3>
        <p><strong>이자 지급 방식:</strong> {{ selectedProduct?.optionList.find(o => o.save_trm === '1')?.intr_rate_type_nm || '복리' }}</p>
        <p style="white-space: pre-line;"><strong>가입 방법:</strong> {{ selectedProduct?.join_way }}</p>
        <p style="white-space: pre-line;"><strong>만기 후 이자율:</strong> {{ selectedProduct?.mtrt_int }}</p>
        <p style="white-space: pre-line;"><strong>우대 조건:</strong> {{ selectedProduct?.spcl_cnd }}</p>
        <p><strong>가입 제한 여부:</strong> {{ joinDenyDetail(selectedProduct?.join_deny) }}</p>
        <p style="white-space: pre-line;"><strong>가입 대상:</strong> {{ selectedProduct?.join_member }}</p>
        <p style="white-space: pre-line;"><strong>기타 참고사항:</strong> {{ selectedProduct?.etc_note }}</p>
        <button @click="closeModal">닫기</button>
        <button @click="addToMyProducts(selectedProduct.fin_prdt_cd)">내 상품에 추가</button>
      </div>
    </teleport>

    <div v-if="paginatedProducts.length" style="margin-top: 1rem">
      <button @click="prevPage" :disabled="currentPage === 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
    </div>
  </div>

  <div style="margin-top: 2rem">
    <h3>추천 조건</h3>
    <label>
      최소 이자율:
      <input type="number" v-model.number="minRate">
    </label>
    <label>
      예치 기간:
      <input type="number" v-model.number="minTerm"> ~ 
      <input type="number" v-model.number="maxTerm"> 개월
    </label>
    <label>
      뱅킹 방식:
      <select v-model="bankingType">
        <option value="">전체</option>
        <option>인터넷</option>
        <option>모바일</option>
        <option>창구</option>
      </select>
    </label>
    <label>
      선호 은행 (콤마 구분):
      <input type="text" v-model="preferredBanks">
    </label>
    <button @click="getRecommendations">추천 상품 보기</button>
  </div>

  <div v-if="recommendedProducts.length" style="margin-top: 1rem">
    <h4>추천 상품 목록</h4>
    <table border="1" style="width: 100%">
      <thead>
        <tr>
          <th>금융회사</th>
          <th>상품명</th>
          <th>이자 유형</th>
          <th>기간</th>
          <th>금리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in recommendedProducts" :key="p.fin_prdt_cd">
          <td>{{ p.kor_co_nm }}</td>
          <td>{{ p.fin_prdt_nm }}</td>
          <td>{{ p.optionList[0]?.intr_rate_type_nm }}</td>
          <td>{{ p.optionList[0]?.save_trm }}개월</td>
          <td>{{ p.optionList[0]?.intr_rate }}%</td>
        </tr>
      </tbody>
    </table>
  </div>


</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useDepositView } from '@/stores/depositview'
import { useAccountStore } from '@/stores/accounts'
const accountStore = useAccountStore()

///// 추천 /////
import { ref } from 'vue'

const minRate = ref(2.0)
const minTerm = ref(6)
const maxTerm = ref(24)
const bankingType = ref('')
const preferredBanks = ref('신한은행,국민은행')
const recommendedProducts = ref([])

const isTermView = ref(true)  // 예금이면 true, 적금이면 false

const getRecommendations = async () => {
  const productType = isTermView.value ? 'term' : 'saving'

  const params = new URLSearchParams({
    product_type: productType,
    min_rate: minRate.value,
    min_term: minTerm.value,
    max_term: maxTerm.value,
    banking_type: bankingType.value,
    preferred_banks: preferredBanks.value
  })

  const headers = {
    Authorization: `Token ${accountStore.token}`
  }

  const res = await fetch(`http://localhost:8000/api/fin-products/recommend/product-based/?${params}`, {
    headers
  })

  if (!res.ok) {
    console.error('추천 API 오류:', res.status)
    return
  }

  recommendedProducts.value = await res.json()
}

// const getRecommendations = async () => {
//   const productType = isTermView.value ? 'term' : 'saving'

//   const params = new URLSearchParams({
//     product_type: productType,
//     min_rate: minRate.value,
//     min_term: minTerm.value,
//     max_term: maxTerm.value,
//     banking_type: bankingType.value,
//     preferred_banks: preferredBanks.value
//   })

//   const res = await fetch(`http://localhost:8000/api/fin-products/recommend/product-based/?${params}`)
//   recommendedProducts.value = await res.json()
// }
//////////////

const store = useDepositView()

const {
  selectedProduct, showModal, filterBank, filterTerm,
  currentPage, totalPages, paginatedProducts
} = storeToRefs(store)

const {
  openProductModal, closeModal, joinDenyDetail,
  nextPage, prevPage, sortByTerm, getRateByTerm,
  loadTerm, loadSaving, addToMyProducts,
} = store

onMounted(async () => {
  try {
    // 1. 데이터 저장 요청 (없으면 생략 가능)
    await fetch('http://localhost:8000/api/fin-products/fetch/term_deposits/', {
      method: 'POST'
    })

    // 2. 저장 후 렌더링용 데이터 요청
    await loadTerm()
  } catch (err) {
    console.error('예금 데이터 저장 또는 로딩 실패:', err)
  }
})
</script>


<style>
.modal {
  all: unset;
  position: fixed !important;
  top: 50px !important;
  left: 50px !important;
  background: white !important;
  padding: 2rem !important;
  border: 3px solid rgb(17, 4, 4) !important;
  z-index: 999999 !important;
  width: 500px !important;
  height: auto !important;
  display: block !important;
  box-shadow: 0 0 20px black !important;
}

</style>
