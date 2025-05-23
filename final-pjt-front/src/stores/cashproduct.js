// stores/cashproduct.js
import { defineStore } from 'pinia'
import axios from 'axios'

// 보류 이유: 주말이나 공휴일은 뛰어 넘어버린다. 
// export const useCashProductStore = defineStore('cashproduct', {
//   state: () => ({
//     prices: {},
//     currentPrice: {},
//     startDate: '',
//     endDate: ''
//   }),
//   actions: {
//     setDateRange(days) {
//       const end = new Date()
//       const start = new Date()
//       start.setDate(end.getDate() - days)

//       this.startDate = start.toISOString().split('T')[0]
//       this.endDate = end.toISOString().split('T')[0]
//     },
//     async fetchPrices(type, period = '1mo') {
//       const params = this.startDate && this.endDate
//         ? { start: this.startDate, end: this.endDate }
//         : { period }

//       const res = await axios.get(`http://localhost:8000/api/raw-products/${type}-price/`, { params })

//       this.prices[type] = res.data.prices
//       this.currentPrice[type] = res.data.prices.at(-1)?.price || null
//     }
//   }
// })

// 날짜 보정 함수 (토요일 → 금요일, 일요일 → 월요일)
function adjustToNearestWeekday(dateStr) {
  const date = new Date(dateStr)
  const day = date.getDay()

  if (day === 6) {
    date.setDate(date.getDate() - 1)  // 토요일 -> 금요일
  } else if (day === 0) {
    date.setDate(date.getDate() + 1)  // 일요일 -> 월요일
  }

  return date.toISOString().split('T')[0]
}

export const useCashProductStore = defineStore('cashproduct', {
  state: () => ({
    prices: {},
    currentPrice: {},
    startDate: '',
    endDate: ''
  }),

  actions: {
    // preset 버튼용 날짜 설정 (자동 평일 조정 포함)
    setDateRange(days) {
      const today = new Date()
      const end = new Date(today)
      const start = new Date()
      start.setDate(end.getDate() - days)

      this.startDate = adjustToNearestWeekday(start.toISOString().split('T')[0])
      this.endDate = adjustToNearestWeekday(end.toISOString().split('T')[0])
    },

    // 📌 사용자가 수동 입력한 날짜도 조회 직전에 보정
    adjustDatesToWeekdays() {
      this.startDate = adjustToNearestWeekday(this.startDate)
      this.endDate = adjustToNearestWeekday(this.endDate)
    },

    async fetchPrices(type, period = '1mo') {
      const params = this.startDate && this.endDate
        ? { start: this.startDate, end: this.endDate }
        : { period }

      const res = await axios.get(`http://localhost:8000/api/raw-products/${type}-price/`, { params })
      this.prices[type] = res.data.prices
      this.currentPrice[type] = res.data.prices.at(-1)?.price || null
    }
  }
})
