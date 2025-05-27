<template>
  <div>
    <div style="display: flex; gap: 0.5rem; align-items: center">
      <h2 @click="() => { isTermView = true; loadTerm() }" style="cursor: pointer">정기예금</h2>
      <button @click="store.fetchAndStoreTermProducts">정기예금 최신화</button>
      <h2>|</h2>
      <h2 @click="() => { isTermView = false; loadSaving() }" style="cursor: pointer">적금</h2>
      <button @click="store.fetchAndStoreSavingProducts">적금 최신화</button>
    </div>

    <div class="form-group">
      <label>금융회사명:</label>
      <input type="text" v-model="filterBank" placeholder="금융회사 명을 적으세요" />
    </div>

    <div class="form-group">
      <label>예치기간:</label>
      <select v-model="filterTerm">
        <option value="">전체</option>
        <option value="1">1개월</option>
        <option value="3">3개월</option>
        <option value="6">6개월</option>
        <option value="12">12개월</option>
        <option value="24">24개월</option>
        <option value="36">36개월</option>
      </select>
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
        <tr v-for="product in paginatedProducts" :key="product.fin_prdt_cd + '-' + product.fin_co_no"
          @click="openProductModal(product)" style="cursor: pointer">
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
        <button @click="handleAddToMyProducts">내 상품에 추가</button>
      </div>
    </teleport>

    <div v-if="paginatedProducts.length" style="margin-top: 1rem">
      <button @click="prevPage" :disabled="currentPage === 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
    </div>

    <div style="margin-top: 2rem">
      <h3>추천 조건</h3>

      <div class="form-group">
        <label>최소 이자율:</label>
        <input type="number" v-model.number="minRate" />
      </div>

      <div class="form-group">
        <label>예치 기간:</label>
        <div style="display: flex; gap: 0.5rem; align-items: center">
          <input type="number" v-model.number="minTerm" /> ~
          <input type="number" v-model.number="maxTerm" /> 개월
        </div>
      </div>

      <div class="form-group">
        <label>뱅킹 방식:</label>
        <select v-model="bankingType">
          <option value="">전체</option>
          <option>인터넷</option>
          <option>모바일</option>
          <option>창구</option>
        </select>
      </div>

      <div class="form-group">
        <label>선호 은행 (콤마 구분):</label>
        <input type="text" v-model="preferredBanks" />
      </div>

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
            <td>{{ getMatchedOption(p)?.save_trm }}개월</td>
            <td>{{ getMatchedOption(p)?.intr_rate }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
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

const minRate = ref('')
const minTerm = ref('')
const maxTerm = ref('')
const bankingType = ref('')
const preferredBanks = ref('')
const recommendedProducts = ref([])

const isTermView = ref(true)

const getRecommendations = async () => {
  const productType = isTermView.value ? 'term' : 'saving'

  const minRateVal = parseFloat(minRate.value)
  const minTermVal = parseInt(minTerm.value)
  const maxTermVal = parseInt(maxTerm.value)

  if (isNaN(minRateVal) || isNaN(minTermVal) || isNaN(maxTermVal)) {
    alert('모든 필드를 올바르게 입력해주세요.')
    return
  }

  if (minRateVal < 0) {
    alert('최소 이자율은 0 이상이어야 합니다.')
    return
  }

  if (minTermVal > maxTermVal) {
    alert('예치 최소 기간은 최대 기간보다 작거나 같아야 합니다.')
    return
  }

  const params = new URLSearchParams({
    product_type: productType,
    min_rate: minRateVal,
    min_term: minTermVal,
    max_term: maxTermVal,
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

const handleAddToMyProducts = () => {
  const productId = selectedProduct.value.fin_prdt_cd
  const productType = isTermView.value ? 'term' : 'saving'
  addToMyProducts(productId, productType)
}

// 상품 옵션 중 조건에 맞는 것 찾기
const getMatchedOption = (product) => {
  const min = parseInt(minTerm.value)
  const max = parseInt(maxTerm.value)
  const rate = parseFloat(minRate.value)

  const matched = product.optionList
    .filter(opt => {
      const term = parseInt(opt.save_trm)
      return term >= min && term <= max && opt.intr_rate >= rate
    })
    .sort((a, b) => b.intr_rate - a.intr_rate)  // 높은 금리 우선 정렬

  return matched[0] || product.optionList[0]
}


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

<style>

input, select, textarea {
  width: 100%;
  padding: 0.6rem;
  border-radius: 0.5rem;
  border: 1px solid #ccc;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

button {
  background-color: #FFD700;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #e6c200;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

</style>