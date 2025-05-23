<template>
  <div>
    <h2 @click="loadTerm">정기예금</h2>
    <h2 @click="loadSaving">적금</h2>

    <table v-if="products.length" border="1" style="width: 100%; border-collapse: collapse">
      <thead>
        <tr>
          <th>공시 제출월</th>
          <th>금융회사명</th>
          <th>상품명</th>
          <th>1개월</th>
          <th>3개월</th>
          <th>6개월</th>
          <th>12개월</th>
          <th>24개월</th>
          <th>36개월</th>
        </tr>
      </thead>
      <tbody>
        <!-- 오류 걸릴 경우: 키를 (:key="product.fin_prdt_cd") 로 바꾸기 -->
        <tr v-for="product in paginatedProducts" :key="product.fin_prdt_cd + '-' + product.fin_co_no"> 
          <td>{{ product.dcls_month }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ getRateByTerm(product, "1") }}</td>
          <td>{{ getRateByTerm(product, "3") }}</td>
          <td>{{ getRateByTerm(product, "6") }}</td>
          <td>{{ getRateByTerm(product, "12") }}</td>
          <td>{{ getRateByTerm(product, "24") }}</td>
          <td>{{ getRateByTerm(product, "36") }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="products.length" style="margin-top: 1rem">
      <button @click="prevPage" :disabled="currentPage === 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"

////////// 페이지 넘기는 기능 ///////////
const currentPage = ref(1);
const pageSize = 10

const totalPages = computed(() => Math.ceil(products.value.length / pageSize))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return products.value.slice(start, start + pageSize)
});

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}
///////////////////////////////////

// 6 ~ 36개월 할당 도움 함수///
function getRateByTerm(product, term) {
  const option = product.optionList.find((o) => o.save_trm === term);
  return option ? option.intr_rate : "-"
}
///////////////////////////////////

//////////필터//////////
// 은행 필터
// 예치기간 필터
// 희망 이율 구간 
/////////////////////

///////////정렬///////////
// 각 개월의 이율에 따라 처음 누를 때는 오름차순, 또 누르먄 내림차순 이후 반복

//////////// 렌더링 및 누를 때 전환되도록 ////////////
const products = ref([])

onMounted(async () => {
  try {
    const res_term = await fetch("http://localhost:8000/api/fin-products/term_deposits/")
    const data = await res_term.json()
    console.log("API 응답:", data.result.length)

    products.value = data.result
  } catch (err) {
    console.error("API 호출 실패:", err)
  }
})

async function loadTerm() {
  try {
    const res = await fetch("http://localhost:8000/api/fin-products/term_deposits/")
    const data = await res.json()
    products.value = data.result
    currentPage.value = 1
  } catch (err) {
    console.error("정기예금 API 호출 실패:", err)
  }
}

async function loadSaving() {
  try {
    const res = await fetch("http://localhost:8000/api/fin-products/saving_deposits/")
    const data = await res.json()
    products.value = data.result
    currentPage.value = 1
  } catch (err) {
    console.error("적금 API 호출 실패:", err)
  }
}
/////////////////////////////////////////////
</script>

<style scoped></style>
