import { createRouter, createWebHistory } from 'vue-router'
import DepositView from '@/views/DepositView.vue'
import CashProduct from '@/views/CashProduct.vue'
import BankMap from '@/views/BankMap.vue'
import ArticlesList from '@/views/ArticlesList.vue'
import LogInView from '@/views/LogInView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/comparisonDeposit',
      name: 'comparisonDeposit',
      component: DepositView,
    },
    {
      path: '/cashProduct',
      name: 'cashProduct',
      component: CashProduct,
    },
    {
      path: '/bankMap',
      name: 'bankMap',
      component: BankMap,
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticlesList,
    },
    {
      path: '/logIn',
      name: 'logIn',
      component: LogInView,
    },
  ],
})

export default router
