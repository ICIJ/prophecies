import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'

export const router = {
  routes: [
    {
      name: 'home',
      path: '/',
      component: Home,
      meta: {
        title: 'Home'
      }
    },
    {
      name: 'login',
      path: '/login',
      component: Login,
      meta: {
        title: 'Login'
      }
    },
    {
      name: 'error',
      path: '*',
      meta: {
        title: 'Something went wrong'
      }
    }
  ]
}

export default router
