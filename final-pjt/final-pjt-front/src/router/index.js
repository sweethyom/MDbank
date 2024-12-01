import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ProductView from '@/views/ProductView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import ProfileView from '@/views/ProfileView.vue'
import { useMemberStore } from '@/stores/modules/member'
import KakaoMapView from '@/views/KakaoMapView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import AssetTypeView from '@/views/AssetTypeView.vue'
import HelpView from '@/views/HelpView.vue'
import QandAView from '@/views/QandAView.vue'
import FaqView from '@/views/FaqView.vue'
import QandADetailView from '@/views/QandADetailView.vue'
import QandACreateView from '@/views/QandACreateView.vue'
import QandAUpdateView from '@/views/QandAUpdateView.vue'
import TransferView from '@/views/TransferView.vue'
import TransferHistoryView from '@/views/TransferHistoryView.vue'
import ProfileChangeView from '@/views/ProfileChangeView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/product',
      name: 'ProductView',
      component: ProductView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
    },
    {
      path: '/profilechange',
      name: 'ProfileChangeView',
      component: ProfileChangeView,
    },
    {
      path: '/exchange',
      name: 'ExchangeView',
      component: ExchangeView,
    },
    {
      path: '/map',
      name: 'KakaoMapView',
      component: KakaoMapView,
    },
    {
      path: '/product/:id',  // :id는 동적 파라미터
      name: 'ProductDetailView',
      component: ProductDetailView,
      props: true  // URL 파라미터를 컴포넌트의 props로 전달
    },
    {

      path: '/transfer',
      name: 'TransferView',
      component: TransferView,
    },
    {
      path: '/assttype',
      name: 'AssetTypeView',
      component: AssetTypeView,
    },
    {
      path: '/transferhistory',
      name: 'TransferHistoryView',
      component: TransferHistoryView,
    },
    {
      path: '/help',
      name: 'HelpView',
      component: ()=> import('@/views/HelpView.vue'),
      children:[
        {
          path: '/qna',
          name: 'QandAView',
          component: QandAView,
        },
        {
          path: '/faq',
          name: 'FaqView',
          component: FaqView,
        },
        {
          path: '/create',
          name: 'QandACreateView',
          component: QandACreateView,
        },
        {
          path: '/qanda/:id',
          name: 'QandADetailView',
          component: QandADetailView,
          props: true
        },
        {
          path: '/qanda/update/:id',
          name: 'QandAUpdateView',
          component: QandAUpdateView,
        },
      ]
    },

  ],
})
//인증 되지 않은 사용자는 메인페이지 접근 제한
router.beforeEach((to,from)=>{

  const store = useMemberStore()
  // 로그인 한 사람만 접근 가능
  if ((to.name === 'ProfileView'|| to.name === 'AssetTypeView' || to.name === 'TransferView' || to.name === 'TransferHistoryView') 
    && !store.isLogin){
    window.alert('로그인이 필요합니다')
    return {name:'LoginView'}
  }
  // 로그인된 사람은 접근 못함
  if((to.name === 'SignUpView' || to.name === 'LoginView')&&(store.isLogin)){
    window.alert('이미 로그인이 되었습니다.')
    return {name:'HomeView'}
  }

})


export default router
