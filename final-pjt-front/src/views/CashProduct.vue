<template>
  <h1>현물 상품</h1>

  <!-- 전환 버튼 -->
  <div>
    <button @click="selectedAsset = 'gold'">금 가격</button>
    <button @click="selectedAsset = 'silver'">은 가격</button>
  </div>

  <!-- 아래는 전환 버튼 눌렀을 때 나올 차트 -->
  <div v-if="selectedAsset === 'gold'">
    <h2>금 시세 (${{ currentPrices.gold || "-" }})</h2>
    <div>
      <button @click="loadChart('1d')">3일</button>
      <button @click="loadChart('5d')">7일</button>
      <button @click="loadChart('1mo')">1개월</button>
      <button @click="loadChart('1y')">1년</button>
    </div>
    <canvas id="goldChart"></canvas>
  </div>

  <div v-if="selectedAsset === 'silver'">
    <h2>은 시세 (${{ currentPrices.silver || "-" }})</h2>
    <div>
      <button @click="loadChart('1d')">3일</button>
      <button @click="loadChart('5d')">7일</button>
      <button @click="loadChart('1mo')">1개월</button>
      <button @click="loadChart('1y')">1년</button>
    </div>
    <canvas id="silverChart"></canvas>
  </div>

</template>

<script setup>
import { watch, ref, nextTick } from "vue"
import Chart from "chart.js/auto"

const selectedAsset = ref("gold");
const charts = {}; // 차트 인스턴스 저장용
const currentPrices = ref({}); // 금, 은 가격 저장용

const loadChart = async (type, period = "1mo") => {
  await nextTick() // 먼저 DOM 렌더 보장, canvas 렌더링 보장

  const res = await fetch(
    `http://localhost:8000/api/raw-products/${type}-price/?period=${period}`
  );
  if (!res.ok) {
    console.error(`${type} 데이터 요청 실패`)
    return;
  }
  const data = await res.json()

  const labels = data.prices.map((p) => p.date)
  const prices = data.prices.map((p) => p.price)

  currentPrices.value[type] = prices[prices.length - 1]

  // 기존 차트 제거
  if (charts[type]) charts[type].destroy()

  const ctx = document.getElementById(`${type}Chart`)
  if (!ctx) {
    console.warn(`${type}Chart 캔버스 찾을 수 없음`)
    return
  }

  charts[type] = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: `${type.toUpperCase()} Price (${period})`,
          data: prices,
          borderWidth: 2,
          tension: 0.3,
        },
      ],
    },
  })
}

// 값이 바뀌면 차트 전환되도록
watch(
  selectedAsset,
  (newAsset) => {
    loadChart(newAsset, "1mo");
  },
  { immediate: true }
)

// onMounted로 전환 시 import 바꾸기
// onMounted(() => {
//   loadChart('gold', '1mo')
//   loadChart('silver', '1mo')
// })
</script>

<style scoped>
</style>