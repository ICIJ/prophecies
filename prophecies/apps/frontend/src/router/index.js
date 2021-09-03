import Dashboard from '@/views/Dashboard.vue'
import Error from '@/views/Error.vue'
import Login from '@/views/Login.vue'
import TaskRecordReviewList from '@/views/TaskRecordReviewList.vue'
import TaskRecordReviewRetreive from '@/views/TaskRecordReviewRetreive.vue'
import TipList from '@/views/TipList.vue'

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
      name: 'task-record-review-list',
      path: '/task-record-reviews/:taskId',
      component: TaskRecordReviewList,
      props: true
    },
    {
      name: 'task-record-review-retreive',
      path: '/task-record-reviews/:taskId/:taskRecordReviewId',
      component: TaskRecordReviewRetreive,
      props: true
    },
    {
      name: 'tip-list',
      path: '/tips',
      component: TipList,
      props: true
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
