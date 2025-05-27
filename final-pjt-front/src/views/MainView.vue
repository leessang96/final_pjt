fixed_4col_main_view = """
<template>
  <div class="main-container">
    <header class="header">
      <h1 class="logo">ban(k)pick</h1>
      <p class="subtitle">내게 맞는 금융 상품을 쉽고 똑똑하게 찾는 방법</p>
    </header>

    <section class="features-grid">
      <div class="feature-card" v-for="(feature, idx) in features" :key="idx">
        <div class="icon">💡</div>
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.description }}</p>
      </div>
    </section>

    <section class="cta">
      <RouterLink to="/comparisonDeposit">
        <button class="main-button">💳 금융 상품 비교하러 가기</button>
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const features = ref([
  { title: '정기예금 비교', description: '다양한 은행의 예금 상품을 금리순으로 비교합니다.' },
  { title: '적금 상품 추천', description: '내 정보에 맞는 적금 상품을 추천받아보세요.' },
  { title: '자산 기반 추천', description: '자산 정보를 기반으로 전략을 설계합니다.' },
  { title: '은행 지도 찾기', description: '가까운 은행 지점을 지도에서 쉽게 확인하세요.' }
])

onMounted(() => {
  const hasFetched = localStorage.getItem('hasFetchedProducts')
  if (!hasFetched) {
    fetch('http://localhost:8000/api/fin-products/fetch/term_deposits/', { method: 'POST' })
    fetch('http://localhost:8000/api/fin-products/fetch/saving_deposits/', { method: 'POST' })
    localStorage.setItem('hasFetchedProducts', 'true')
  }
})
</script>

<style>
.main-container {
  padding: 4rem 2rem;
  background: #fffef8;
  text-align: center;
  font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
}

.logo {
  font-size: 3.8rem;
  color: #FFCB05;
  font-weight: 900;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #555;
  font-size: 1.15rem;
  margin-bottom: 3rem;
  font-weight: 400;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  margin-bottom: 3.5rem;
  max-width: 1100px;
  margin-inline: auto;
  overflow-x: auto;
}

.feature-card {
  background: #ffffff;
  padding: 2.2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  transition: all 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.feature-card .icon {
  font-size: 2.2rem;
  margin-bottom: 1rem;
  color: #FFCB05;
}

.feature-card h3 {
  font-size: 1.25rem;
  color: #222;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.feature-card p {
  color: #555;
  font-size: 0.95rem;
  font-weight: 400;
  line-height: 1.5;
}

.main-button {
  font-size: 1.15rem;
  padding: 1rem 2.5rem;
  background-color: #FFCB05;
  border: none;
  border-radius: 1.5rem;
  font-weight: 600;
  color: #222;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.main-button:hover {
  background-color: #e5b800;
}
</style>