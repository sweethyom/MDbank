import BankingCreateView from '@/views/BankingCreateView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import BalanceCreateView from '@/views/BalanceCreateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView,
    // },
    {
      path: '/create',
      name: 'BankingCreateView',
      component:BankingCreateView
    },
    {
      path: '/balance',
      name: 'BalanceCreateView',
      component:BalanceCreateView
    }
  ],
})

export default router
