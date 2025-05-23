<template>
  <h1>현물 상품</h1>

  <!-- 전환 버튼 -->
  <div>
    <button @click="selectedAsset = 'gold'">금 가격</button>
    <button @click="selectedAsset = 'silver'">은 가격</button>
  </div>

  <!-- 금 -->
  <div v-if="selectedAsset === 'gold'">
    <h2>금 시세 (${{ cashproduct.currentPrice.gold || "-" }})</h2>

    <div>
      <label>시작일
        <input type="date" v-model="cashproduct.startDate">
      </label>
      <label>종료일
        <input type="date" v-model="cashproduct.endDate">
      </label>
      <button @click="loadCustomDateChart('gold')">조회</button>
    </div>

    <canvas id="goldChart"></canvas>
  </div>

  <!-- 은 -->
  <div v-if="selectedAsset === 'silver'">
    <h2>은 시세 (${{ cashproduct.currentPrice.silver || "-" }})</h2>

    <div>
      <label>시작일
        <input type="date" v-model="cashproduct.startDate">
      </label>
      <label>종료일
        <input type="date" v-model="cashproduct.endDate">
      </label>
      <button @click="loadCustomDateChart('silver')">조회</button>
    </div>

    <canvas id="silverChart"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import { useCashProductStore } from '@/stores/cashproduct'

const cashproduct = useCashProductStore()
const selectedAsset = ref('gold')
const charts = {}

const loadChart = async (type) => {
  await nextTick()
  await cashproduct.fetchPrices(type)

  const priceData = cashproduct.prices[type]
  const labels = priceData.map(p => p.date)
  const prices = priceData.map(p => p.price)

  if (charts[type]) charts[type].destroy()
  const ctx = document.getElementById(`${type}Chart`)
  if (!ctx) return

  charts[type] = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: `${type.toUpperCase()} Price`,
        data: prices,
        borderWidth: 2,
        tension: 0.3
      }]
    }
  })
}

const loadCustomDateChart = async (type) => {
  const todaySTR = new Date().toISOString().split('T')[0]

  if (!cashproduct.startDate || !cashproduct.endDate) {
    alert("시작일과 종료일을 선택해주세요.")
    return
  }
  if (cashproduct.startDate > cashproduct.endDate) {
    alert("종료일이 시작일보다 빠릅니다.")
    return
  }

  if (cashproduct.startDate > todaySTR || cashproduct.endDate > todaySTR){
    alert("미래 가격은 알 순 없습니다.")
    return
  }

  cashproduct.adjustDatesToWeekdays()
  await loadChart(type)
}

watch(selectedAsset, (newAsset) => {
  loadChart(newAsset)
}, { immediate: true })
</script>

<style scoped>
button {
  margin-right: 0.5rem;
}
</style>
