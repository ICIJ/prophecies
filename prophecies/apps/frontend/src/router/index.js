import Dashboard from '@/views/Dashboard'
import Error from '@/views/Error'
import Login from '@/views/Login'
import History from '@/views/History'
import ShortcutList from '@/views/ShortcutList'
import TaskRecordReviewList from '@/views/TaskRecordReviewList'
import TaskRecordReviewRetrieve from '@/views/TaskRecordReviewRetrieve'
import TipList from '@/views/TipList'
import TipRetrieve from '@/views/TipRetrieve'
import StatsList from '@/views/StatsList'
import UserRetrieve from '@/views/UserRetrieve'
import UserRetrieveProfile from '@/views/UserRetrieveProfile'
import UserRetrieveLanguage from '@/views/UserRetrieveLanguage'
import UserRetrieveActivity from '@/views/UserRetrieveActivity'
import UserRetrieveTeam from '@/views/UserRetrieveTeam'
import UserRetrieveBookmarks from '@/views/UserRetrieveBookmarks'
import UserRetrieveNotifications from '@/views/UserRetrieveNotifications'
import UserRetrieveHistory from '@/views/UserRetrieveHistory'

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
        },
        {
          name: 'user-retrieve-activity',
          path: 'activity',
          component: UserRetrieveActivity,
          props: (route) => ({ query: route.query, username: route.params.username })
        },
        {
          name: 'user-retrieve-team',
          path: 'team',
          props: true,
          component: UserRetrieveTeam
        },
        {
          name: 'user-retrieve-bookmarks',
          path: 'bookmarks',
          component: UserRetrieveBookmarks,
          props: (route) => ({ query: route.query, username: route.params.username })
        },
        {
          name: 'user-retrieve-notifications',
          path: 'notifications',
          component: UserRetrieveNotifications,
          props: true
        },
        {
          name: 'user-retrieve-history',
          path: 'history',
          component: UserRetrieveHistory,
          props: true
        },
        {
          name: 'user-retrieve-language',
          path: 'language',
          component: UserRetrieveLanguage,
          props: true
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
      path: '/tasks',
      component: StatsList,
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
