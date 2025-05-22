<template>
  <h1>현물 상품</h1>
      <div>
        <h2>금 시세 (${{ CurrentPrice }})</h2>
        <div>
            <button @click="loadChart('1d')">1일</button>
            <button @click="loadChart('5d')">5일</button>
            <button @click="loadChart('1mo')">1개월</button>
            <button @click="loadChart('1y')">1년</button>
        </div>
        <canvas id="goldChart"></canvas>

        <div>
        <h2>은 시세</h2>
        <div>
            <button @click="loadChart('1d')">1일</button>
            <button @click="loadChart('5d')">5일</button>
            <button @click="loadChart('1mo')">1개월</button>
            <button @click="loadChart('1y')">1년</button>
        </div>
        <canvas id="silverChart"></canvas>
        </div>
      </div>
</template>

<script setup>
//   // 주기적으로 데이터 요청 (5초마다)
//   fetchGoldPrice()
//   setInterval(fetchGoldPrice, 5000)
// })

import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'
import { nextTick } from 'vue' // 추가 부분 

let chart = null
const CurrentPrice = ref(null)

const charts = {}               // 차트 인스턴스 저장용
const currentPrices = ref({})  // 금, 은 가격 저장용

const loadChart = async (type, period = '1mo') => {
  const res = await fetch(`http://localhost:8000/api/raw-products/${type}-price/?period=${period}`)
  if (!res.ok) {
    console.error(`${type} 데이터 요청 실패`)
    return
  }
  const data = await res.json()

  const labels = data.prices.map(p => p.date)
  const prices = data.prices.map(p => p.price)

  currentPrices.value[type] = prices[prices.length - 1]

  // 기존 차트 제거
  if (charts[type]) charts[type].destroy()

  await nextTick()  // canvas 렌더링 보장

  const ctx = document.getElementById(`${type}Chart`)
  if (!ctx) {
    console.warn(`${type}Chart 캔버스 찾을 수 없음`)
    return
  }

  charts[type] = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: `${type.toUpperCase()} Price (${period})`,
        data: prices,
        borderWidth: 2,
        tension: 0.3,
      }]
    }
  })
}

onMounted(() => {
  loadChart('gold', '1mo')
  loadChart('silver', '1mo')
})
</script>

<style scoped>

</style>