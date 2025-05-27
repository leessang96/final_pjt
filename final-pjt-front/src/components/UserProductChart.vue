<template>
  <div>
    <h3>가입한 상품들</h3>
    <ol>
      <li v-for="(p, index) in allProducts" :key="p.fin_prdt_cd">
        {{ index + 1 }} : ({{ p.typeLabel }}){{ p.kor_co_nm }} - <strong>{{ p.fin_prdt_nm }}</strong>
    </li>
    </ol>

    <h3>가입한 상품 금리</h3>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  termProducts: Array,
  savingProducts: Array
})

// 예금/적금 통합 배열 만들기
const allProducts = [
  ...(props.termProducts || []).map(p => ({ ...p, typeLabel: '예금' })),
  ...(props.savingProducts || []).map(p => ({ ...p, typeLabel: '적금' }))
]

console.log(allProducts)

const chartData = {
  labels: allProducts.map(p => p.fin_prdt_nm),
  datasets: [
    {
      label: '저축 금리',
      backgroundColor: 'skyblue',
      data: allProducts.map(p => p.optionList?.[0]?.intr_rate || 0)
    },
    {
      label: '최고 우대금리',
      backgroundColor: 'lightgreen',
      data: allProducts.map(p => p.optionList?.[0]?.intr_rate2 || 0)
    }
  ]
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: false
    }
  }
}
</script>
