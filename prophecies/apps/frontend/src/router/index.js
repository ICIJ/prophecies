import Dashboard from '@/views/Dashboard.vue'
import Error from '@/views/Error.vue'
import Login from '@/views/Login.vue'
import History from '@/views/History.vue'
import ShortcutList from '@/views/ShortcutList.vue'
import TaskRecordReviewList from '@/views/TaskRecordReviewList.vue'
import TaskRecordReviewRetrieve from '@/views/TaskRecordReviewRetrieve.vue'
import TipList from '@/views/TipList.vue'
import TipRetrieve from '@/views/TipRetrieve.vue'
import StatsList from '@/views/StatsList.vue'
import UserRetrieve from '@/views/UserRetrieve.vue'
import UserRetrieveProfile from '@/views/UserRetrieveProfile.vue'
import Bookmarks from '@/views/Bookmarks'

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
      path: '/users/:username',
      component: UserRetrieve,
      props: true,
      children: [
        {
          name: 'user-retrieve-profile',
          path: '',
          props: true,
          component: UserRetrieveProfile
        }
      ]
    },
    {
      name: 'history',
      path: '/history',
      component: History,
      props: true
    },
    {
      name: 'shortcut-list',
      path: '/shortcuts',
      component: ShortcutList,
      props: true
    },
    {
      name: 'task-record-review-list',
      path: '/task-record-reviews/:taskId',
      component: TaskRecordReviewList,
      props: true
    },
    {
      name: 'task-record-review-retrieve',
      path: '/task-record-reviews/:taskId/:taskRecordReviewId',
      component: TaskRecordReviewRetrieve,
      props: true
    },
    {
      name: 'tip-list',
      path: '/tips',
      component: TipList,
      props: (route) => ({ query: route.query })
    },
    {
      name: 'stats-list',
      path: '/stats',
      component: StatsList,
      props: true
    },
    {
      name: 'bookmarks',
      path: '/bookmarks',
      component: Bookmarks,
      props: true
    },
    {
      name: 'tip-retrieve',
      path: '/tips/:tipId',
      component: TipRetrieve,
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
