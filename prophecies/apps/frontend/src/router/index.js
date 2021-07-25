import Boilerplate from '@/views/Boilerplate.vue'
import Dashboard from '@/views/Dashboard.vue'
import Error from '@/views/Error.vue'
import Login from '@/views/Login.vue'

export const router = {
  routes: [
    {
      name: 'dashboard',
      path: '/',
      component: Dashboard,
      meta: {
        title: ({ i18n }) => i18n.t('dashboard.title')
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
        title: ({ i18n }) => i18n.t('login.title')
      }
    },
    {
      name: 'error',
      path: '*',
      props: true,
      component: Error,
      meta: {
        title: ({ i18n }) => i18n.t('error.title')
      }
    }
  ]
}

export default router
