import Boilerplate from '@/views/Boilerplate.vue'
import Dashboard from '@/views/Dashboard.vue'
import Login from '@/views/Login.vue'

export const router = {
  routes: [
    {
      name: 'dashboard',
      path: '/',
      component: Dashboard,
      meta: {
        title: 'Dashboard'
      }
    },
    {
      name: 'boilerplate',
      path: '/boilerplate',
      component: Boilerplate,
      meta: {
        title: 'Boilerplate'
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
