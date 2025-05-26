<template>
  <div>
    <div style="display: flex; gap: 0.5rem; align-items: center">
      <h2 @click="loadTerm" style="cursor: pointer">정기예금</h2>
      <h2>|</h2>
      <h2 @click="loadSaving" style="cursor: pointer">적금</h2>
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
          <th @click="sortByTerm('1')">1개월</th>
          <th @click="sortByTerm('3')">3개월</th>
          <th @click="sortByTerm('6')">6개월</th>
          <th @click="sortByTerm('12')">12개월</th>
          <th @click="sortByTerm('24')">24개월</th>
          <th @click="sortByTerm('36')">36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in paginatedProducts" :key="product.fin_prdt_cd + '-' + product.fin_co_no" @click="openProductModal(product)">
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

    <div v-if="showModal" class="modal">
      <h3>상품 세부 정보</h3>
      <p><strong>이자 지급 방식:</strong> {{ selectedProduct?.optionList.find(o => o.save_trm === '1')?.intr_rate_type_nm || '복리' }}</p>
      <p><strong>가입 방법:</strong> {{ selectedProduct?.join_way }}</p>
      <p><strong>만기 후 이자율:</strong> {{ selectedProduct?.mtrt_int }}</p>
      <p><strong>우대 조건:</strong> {{ selectedProduct?.spcl_cnd }}</p>
      <p><strong>가입 제한 여부:</strong> {{ joinDenyDetail(selectedProduct?.join_deny) }}</p>
      <p><strong>가입 대상:</strong> {{ selectedProduct?.join_member }}</p>
      <p><strong>기타 참고사항:</strong> {{ selectedProduct?.etc_note }}</p>
      <button @click="closeModal">닫기</button>
    </div>

    <div v-if="paginatedProducts.length" style="margin-top: 1rem">
      <button @click="prevPage" :disabled="currentPage === 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
    </div>
  </div>
</template>



<script setup>
import { useDepositView } from '@/stores/depositview.js'

const {
  selectedProduct, showModal, openProductModal, closeModal, joinDenyDetail,
  filterBank, filterTerm,
  currentPage, totalPages, nextPage, prevPage,
  paginatedProducts,
  sortByTerm, getRateByTerm,
  loadTerm, loadSaving
} = useDepositView()
// // import { useDepositView } from '@/stores/depositview.js'

// // const {
// //   // 모달
// //   selectedProduct, showModal, openProductModal, closeModal, joinDenyDetail,

// //   // 필터 및 페이지네이션
// //   filterBank, filterTerm,
// //   currentPage, totalPages, nextPage, prevPage,

// //   // 데이터 및 정렬
// //   products, filteredProducts, paginatedProducts,
// //   sortTerm, sortDirection, sortByTerm,
// //   getRateByTerm,

// //   // API 로딩
// //   loadTerm, loadSaving
// // } = useDepositView()

// // import {useProductStore} from '@/stores/depositview'

// // const store = useProductStore()
// // store.loadTerm()

// import { ref, computed, onMounted, watch } from "vue"

// ///////////////모달///////////////
// const selectedProduct = ref(null)
// const showModal = ref(false)

// function openProductModel(product){
//   selectedProduct.value = product
//   showModal.value = true
//   console.log(selectedProduct)
// }
// function closeModal(){
//   selectedProduct.value = null
//   showModal.value = false
// }
// function joinDenyDetail(code) {
//   switch (code) {
//     case '1':
//       return '일부 가입 제한 있음'
//     case '2':
//       return '제한 없음'
//     case '3':
//       return '기타 제한 조건 있음'
//     case '4':
//       return '외국인 가입 제한'
//     default:
//       return '정보 없ㅇ므'
//   }
// }
// /////////////////////////////////

// //////////필터//////////
// // 은행 필터
// // 예치기간 필터
// // 희망 이율 구간 
// const filterBank = ref('')
// const filterTerm = ref('')

// // 기간 수동 입력 기능 생략
// // const minRate = ref(null)
// // const maxRate = ref(null)
// const filteredProducts = computed(() => {
//   return products.value.filter(product => {
//     const matchedBank = filterBank.value === '' || product.kor_co_nm.includes(filterBank.value)
    
//     const option = filterTerm.value
//       ? product.optionList.find(o => o.save_trm === filterTerm.value)
//       : null
    
//     const rate = option?.intr_rate ?? null

//     const matchedTerm = filterTerm.value === '' || !!option
//     // const matchedMinRate = minRate.value === null || (rate !== null && rate >= minRate.value)
//     // const matchedMaxRate = maxRate.value === null || (rate !== null && rate <= maxRate.value)

//     return matchedBank && matchedTerm // && matchedMinRate && matchedMaxRate
//   })

//   console.log("필터 결과:", filteredProducts.value.length)
// })

// // 금융회사 검색할 때, 페이지 1로 초기화
// watch([filterBank, filterTerm], () => {
//   currentPage.value = 1
// })
// // 필터에 따른 페이지 변화 함수는 페이지 함수 쪽으로 보냄
// /////////////////////

// ////////// 페이지 넘기는 기능 ///////////
// const currentPage = ref(1);
// const pageSize = 10

// // const totalPages = computed(() => Math.ceil(products.value.length / pageSize))

// const paginatedProducts = computed(() => {
//   const start = (currentPage.value - 1) * pageSize
//   // return products.value.slice(start, start + pageSize)
//   return filteredProducts.value.slice(start, start + pageSize)
// })

// // filter 적용에 따른 페이지 변화 반영
// const totalPages = computed(() => Math.ceil(filteredProducts.value.length / pageSize))

// function nextPage() {
//   if (currentPage.value < totalPages.value) {
//     currentPage.value++
//   }
// }

// function prevPage() {
//   if (currentPage.value > 1) {
//     currentPage.value--
//   }
// }

// ///////////////////////////////////

// // 6 ~ 36개월 할당 도움 함수///
// function getRateByTerm(product, term) {
//   const option = product.optionList.find((o) => o.save_trm === term);
//   return option ? option.intr_rate : "-"
// }
// ///////////////////////////////////

// ///////////정렬///////////
// // 각 개월의 이율에 따라 처음 누를 때는 오름차순, 또 누르면 내림차순 이후 반복
// const sortTerm = ref(null)
// const sortDirection = ref("asc")

// function sortByTerm(term) {
//   if (sortTerm.value === term) {
//     // 이미 선택된 항목 → 방향만 바꿈
//     sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc"
//   } else {
//     // 새로운 항목 → 기준 변경 & 기본 오름차순
//     sortTerm.value = term
//     sortDirection.value = "asc"
//   }

//   products.value.sort((a, b) => {
//     const aRate = parseFloat(a.optionList.find(o => o.save_trm === term)?.intr_rate ?? -1)
//     const bRate = parseFloat(b.optionList.find(o => o.save_trm === term)?.intr_rate ?? -1)

//     if (sortDirection.value === "asc") {
//       return aRate - bRate
//     } else {
//       return bRate - aRate
//     }
//   })

//   currentPage.value = 1
// }
// /////////////////////////

// //////////// 렌더링 및 누를 때 전환되도록 ////////////
// const products = ref([])

// onMounted(async () => {
//   try {
//     const res_term = await fetch("http://localhost:8000/api/fin-products/term_deposits/")
//     const data = await res_term.json()
//     console.log("API 응답:", data.result.length)

//     products.value = data.result
//   } catch (err) {
//     console.error("API 호출 실패:", err)
//   }
// })

// async function loadTerm() {
//   try {
//     const res = await fetch("http://localhost:8000/api/fin-products/term_deposits/")
//     const data = await res.json()
//     products.value = data.result
//     currentPage.value = 1
//   } catch (err) {
//     console.error("정기예금 API 호출 실패:", err)
//   }
// }

// async function loadSaving() {
//   try {
//     const res = await fetch("http://localhost:8000/api/fin-products/saving_deposits/")
//     const data = await res.json()
//     products.value = data.result
//     currentPage.value = 1
//   } catch (err) {
//     console.error("적금 API 호출 실패:", err)
//   }
// }
// /////////////////////////////////////////////
</script>


<style scoped>
.modal {
  position: fixed;
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border: 1px solid #ccc;
  padding: 1rem;
  z-index: 1000;
  width: 600px;
}
</style>