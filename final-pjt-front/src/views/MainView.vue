<template>
  <h1>메인페이지가 될 예정</h1>
</template>

<script setup>
import { onMounted } from 'vue'

// 서버 들어올 때 한 번만
onMounted(() => {
  const hasFetched = localStorage.getItem('hasFetchedProducts')
  if (!hasFetched) {
    // 정기예금 저장 요청
    fetch('http://localhost:8000/api/fin-products/fetch/term_deposits/', {
      method: 'POST'
    })

    // 적금 저장 요청
    fetch('http://localhost:8000/api/fin-products/fetch/saving_deposits/', {
      method: 'POST'
    })

    localStorage.setItem('hasFetchedProducts', 'true')
  }
})
</script>


<style scoped>

</style>