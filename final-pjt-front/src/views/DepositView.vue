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

    <p>모달 상태: {{ showModal }}</p>

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
      </div>
    </teleport>

    <div v-if="paginatedProducts.length" style="margin-top: 1rem">
      <button @click="prevPage" :disabled="currentPage === 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
    </div>
  </div>

</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useDepositView } from '@/stores/depositview'

const store = useDepositView()

const {
  selectedProduct, showModal, filterBank, filterTerm,
  currentPage, totalPages, paginatedProducts
} = storeToRefs(store)

const {
  openProductModal, closeModal, joinDenyDetail,
  nextPage, prevPage, sortByTerm, getRateByTerm,
  loadTerm, loadSaving
} = store

onMounted(() => {
  loadTerm()
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
