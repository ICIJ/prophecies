import Dashboard from '@/views/Dashboard.vue'
import Error from '@/views/Error.vue'
import Login from '@/views/Login.vue'
import TaskRecordReviews from '@/views/TaskRecordReviews.vue'

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
      name: 'login',
      path: '/login',
      component: Login,
      meta: {
        title: ({ i18n }) => i18n.t('login.title')
      }
    },
    {
      name: 'task-record-reviews',
      path: '/task-record-reviews/:taskId',
      component: TaskRecordReviews,
      props (route) {
        return { ...route.params, ...route.query }
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
