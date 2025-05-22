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

        <!-- <div>
        <h2>은 시세</h2>
        <div>
            <button @click="loadChart('1d')">1일</button>
            <button @click="loadChart('5d')">5일</button>
            <button @click="loadChart('1mo')">1개월</button>
            <button @click="loadChart('1y')">1년</button>
        </div>
        <canvas id="sliverChart"></canvas>
        </div> -->
      </div>
</template>

<script setup>
//   // 주기적으로 데이터 요청 (5초마다)
//   fetchGoldPrice()
//   setInterval(fetchGoldPrice, 5000)
// })

import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'

let chart = null
const CurrentPrice = ref(null)

const loadChart = async (period = '1mo') => {
  const res = await fetch(`http://localhost:8000/api/raw-products/gold-price/?period=${period}`)
  const data = await res.json()

  const labels = data.prices.map(p => p.date)
  const prices = data.prices.map(p => p.price)

  CurrentPrice.value = prices[prices.length - 1] // 가장 최신 가격 

  if (chart) chart.destroy()

  const ctx = document.getElementById('goldChart')
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: `Gold Price (${period})`,
        data: prices,
        borderWidth: 2,
        tension: 0.3,
      }]
    }
  })
}

onMounted(() => {
  loadChart('1mo')
})
</script>

<style scoped>

</style>