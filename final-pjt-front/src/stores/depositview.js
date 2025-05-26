import { ref, computed, watch, onMounted } from 'vue'

export function useDepositView() {
  const selectedProduct = ref(null)
  const showModal = ref(false)

  function openProductModal(product) {
    selectedProduct.value = product
    showModal.value = true
  }

  function closeModal() {
    selectedProduct.value = null
    showModal.value = false
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

    products.value.sort((a, b) => {
      const aRate = parseFloat(a.optionList.find(o => o.save_trm === term)?.intr_rate ?? -1)
      const bRate = parseFloat(b.optionList.find(o => o.save_trm === term)?.intr_rate ?? -1)
      return sortDirection.value === 'asc' ? aRate - bRate : bRate - aRate
    })

    currentPage.value = 1
  }

  async function loadTerm() {
    try {
      const res = await fetch('http://localhost:8000/api/fin-products/term_deposits/')
      const data = await res.json()
      products.value = data.result
      currentPage.value = 1
    } catch (err) {
      console.error('정기예금 API 호출 실패:', err)
    }
  }

  async function loadSaving() {
    try {
      const res = await fetch('http://localhost:8000/api/fin-products/saving_deposits/')
      const data = await res.json()
      products.value = data.result
      currentPage.value = 1
    } catch (err) {
      console.error('적금 API 호출 실패:', err)
    }
  }

  onMounted(loadTerm)

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
    loadTerm, loadSaving
  }
}
