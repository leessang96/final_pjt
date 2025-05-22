<template>
  <div>
    <h2>금융상품 비교</h2>
    <ul>
      <li v-for="product in products" :key="product.fin_prdt_cd">
        {{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const products = ref([])

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/fin-products/term_deposits/')
    const data = await res.json()
    console.log('API 응답:', data)  

    products.value = data.result.baseList  
  } catch (err) {
    console.error('API 호출 실패:', err)
  }
})
</script>


<style scoped>

</style>