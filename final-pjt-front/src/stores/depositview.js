import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useDepositView = defineStore('depositView', () => {
  const selectedProduct = ref(null)
  const showModal = ref(false)

  function openProductModal(product) {
    console.log('[DEBUG] 모달 열기:', product)
    selectedProduct.value = product
    showModal.value = true
  }

  function closeModal() {
    selectedProduct.value = null
    showModal.value = false
  }

  async function addToMyProducts(productId) {
  try {
    const accountStore = useAccountStore()
    const headers = accountStore.token
      ? { Authorization: `Token ${accountStore.token}` }
      : {}

    await axios.post(
      'http://localhost:8000/api/v1/accounts/add-product/',
      { product_id: productId },
      { headers }
    )
    alert('내 상품에 추가되었습니다!')
  } catch (err) {
    console.error('[ERROR] 상품 추가 실패:', err)
    alert('추가 실패: 로그인 상태를 확인하세요')
    }
  }


  function joinDenyDetail(code) {
    switch (code) {
      case '1': return '일부 가입 제한 있음'
      case '2': return '제한 없음'
      case '3': return '기타 제한 조건 있음'
      case '4': return '외국인 가입 제한'
      default: return '정보 없음'
    }
  }

  const filterBank = ref('')
  const filterTerm = ref('')
  const currentPage = ref(1)
  const pageSize = 10
  const products = ref([])
  const sortTerm = ref(null)
  const sortDirection = ref('asc')

  const filteredProducts = computed(() => {
    return products.value.filter(product => {
      const matchedBank = filterBank.value === '' || product.kor_co_nm.includes(filterBank.value)
      const option = filterTerm.value
        ? product.optionList.find(o => o.save_trm === filterTerm.value)
        : null
      const matchedTerm = filterTerm.value === '' || !!option
      return matchedBank && matchedTerm
    })
  })

  const paginatedProducts = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredProducts.value.slice(start, start + pageSize)
  })

  const totalPages = computed(() => Math.ceil(filteredProducts.value.length / pageSize))

  function nextPage() {
    if (currentPage.value < totalPages.value) currentPage.value++
  }

  function prevPage() {
    if (currentPage.value > 1) currentPage.value--
  }

  function getRateByTerm(product, term) {
    const option = product.optionList.find(o => o.save_trm === term)
    return option ? option.intr_rate : '-'
  }

  function sortByTerm(term) {
    if (sortTerm.value === term) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
    } else {
      sortTerm.value = term
      sortDirection.value = 'asc'
    }

    console.time('sort')
    products.value.sort((a, b) => {
      const aRate = a.rateMap?.[term] ?? -1
      const bRate = b.rateMap?.[term] ?? -1
      return sortDirection.value === 'asc' ? aRate - bRate : bRate - aRate
    })
    console.timeEnd('sort')

    currentPage.value = 1
  }

  async function loadTerm() {
    try {
      const res = await fetch('http://localhost:8000/api/fin-products/term_deposits/')
      const data = await res.json()
      products.value = data.result.map(p => ({
      ...p,
      rateMap: Object.fromEntries(p.optionList.map(o => [o.save_trm, o.intr_rate]))
      }))
      currentPage.value = 1
    } catch (err) {
      console.error('정기예금 API 호출 실패:', err)
    }
  }

  async function loadSaving() {
      try {

        const res = await fetch('http://localhost:8000/api/fin-products/saving_deposits/')
        const data = await res.json()
        products.value = data.result.map(p => ({
          ...p,
          rateMap: Object.fromEntries(p.optionList.map(o => [o.save_trm, o.intr_rate]))
        }))
        currentPage.value = 1
      } catch (err) {
        console.error('적금 API 호출 실패:', err)
      }
  }

  async function fetchAndStoreTermProducts() {
    try {
      const res = await fetch('http://localhost:8000/api/fin-products/fetch/term_deposits/', {
        method: 'POST'
      })
      const data = await res.json()
      console.log('[DEBUG] 정기예금 저장 완료:', data)
    } catch (err) {
      console.error('[ERROR] 정기예금 저장 실패:', err)
    }
  }

  async function fetchAndStoreSavingProducts() {
    try {
      const res = await fetch('http://localhost:8000/api/fin-products/fetch/saving_deposits/', {
        method: 'POST'
      })
      const data = await res.json()
      console.log('[DEBUG] 적금 저장 완료:', data)
    } catch (err) {
      console.error('[ERROR] 적금 저장 실패:', err)
    }
  }

  // watch를 여기 둘 수 있음
  watch([filterBank, filterTerm], () => {
    currentPage.value = 1
  })

  return {
    selectedProduct, showModal, openProductModal, closeModal, joinDenyDetail,
    filterBank, filterTerm,
    currentPage, pageSize, products,
    filteredProducts, paginatedProducts, totalPages,
    sortTerm, sortDirection,
    nextPage, prevPage,
    getRateByTerm, sortByTerm,
    loadTerm, loadSaving,
    fetchAndStoreTermProducts, fetchAndStoreSavingProducts,
    addToMyProducts,
  }
})
