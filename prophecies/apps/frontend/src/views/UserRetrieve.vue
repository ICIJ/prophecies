<script>
import { camelCase, uniqueId } from 'lodash'

import User from '@/models/User'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import PageHeader from '@/components/PageHeader'

export default {
  name: 'UserRetrieve',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    PageHeader
  },
  props: {
    username: {
      type: String
    }
  },
  computed: {
    profileRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-profile', params }
    },
    activityRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-activity', params }
    },
    teamRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-team', params }
    },
    bookmarksRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-bookmarks', params }
    },
    notificationsRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-notifications', params }
    },
    historyRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-history', params }
    },
    languageRoute() {
      const params = { username: this.username }
      return { name: 'user-retrieve-language', params }
    },
    fetchUserLoader() {
      return uniqueId('load-user-')
    },
    title() {
      return this.routeTitle(this.$route.name)
    },
    profileTitle() {
      return this.routeTitle(this.profileRoute.name)
    },
    activityTitle() {
      return this.routeTitle(this.activityRoute.name)
    },
    teamTitle() {
      return this.routeTitle(this.teamRoute.name)
    },
    bookmarksTitle() {
      return this.routeTitle(this.bookmarksRoute.name)
    },
    notificationsTitle() {
      return this.routeTitle(this.notificationsRoute.name)
    },
    historyTitle() {
      return this.routeTitle(this.historyRoute.name)
    },
    languageTitle() {
      return this.routeTitle(this.languageRoute.name)
    },
    user() {
      return User.find(this.username)
    },
    isMe() {
      return this.username === User.me()?.username
    },
    icon() {
      switch (this.title) {
        case this.teamTitle:
          return 'UsersIcon'
        case this.activityTitle:
          return 'ActivityIcon'
        case this.bookmarksTitle:
          return 'BookmarkIcon'
        case this.notificationsTitle:
          return 'BellIcon'
        case this.historyTitle:
          return 'ClockIcon'
        case this.languageTitle:
          return 'GlobeIcon'
        default:
          return 'UserIcon'
      }
    }
  },
  watch: {
    title() {
      if (this.user) {
        this.$core.setPageTitle(this.title)
      }
    },
    async username() {
      await this.fetchUserWithLoader()
    }
  },
  async created() {
    try {
      await this.fetchUserWithLoader()
      this.$core.setPageTitle(this.title)
    } catch (error) {
      const title = this.$t('general.unableToFindThisResource')
      this.$router.replace({ name: 'error', params: { title, error } })
    }
  },
  methods: {
    getRouteKey(route) {
      return camelCase(route)
    },
    getRouteKeyPath(routeKey) {
      if (this.user?.isMe) {
        return [routeKey, 'title', 'yours'].join('.')
      }
      return [routeKey, 'title', 'others'].join('.')
    },
    routeTitle(routeName) {
      const routeKey = this.getRouteKey(routeName)
      const path = this.getRouteKeyPath(routeKey)
      return this.$t(path, this.user)
    },
    fetchUser() {
      return User.api().get(this.username)
    },
    async fetchUserWithLoader() {
      this.$wait.start(this.fetchUserLoader)
      await this.fetchUser()
      this.$wait.end(this.fetchUserLoader)
    }
  }
}
</script>

<template>
  <div class="user-retrieve d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top">
      <template #items>
        <b-nav-item :to="profileRoute" exact :class="{ 'font-weight-bold': title === profileTitle }">
          <user-icon class="mr-3" />
          {{ profileTitle }}
        </b-nav-item>
        <b-nav-item :to="activityRoute" exact :class="{ 'font-weight-bold': title === activityTitle }">
          <activity-icon class="mr-3" />
          {{ activityTitle }}
        </b-nav-item>
        <b-nav-item
          v-if="isMe"
          :to="notificationsRoute"
          exact
          :class="{ 'font-weight-bold': title === notificationsTitle }"
        >
          <bell-icon class="mr-3" />
          {{ notificationsTitle }}
        </b-nav-item>
        <b-nav-item :to="bookmarksRoute" exact :class="{ 'font-weight-bold': title === bookmarksTitle }">
          <bookmark-icon class="mr-3" />
          {{ bookmarksTitle }}
        </b-nav-item>
        <b-nav-item :to="historyRoute" exact :class="{ 'font-weight-bold': title === historyTitle }">
          <clock-icon class="mr-3" />
          {{ historyTitle }}
        </b-nav-item>
        <b-nav-item :to="teamRoute" exact :class="{ 'font-weight-bold': title === teamTitle }">
          <users-icon class="mr-3" />
          {{ teamTitle }}
        </b-nav-item>
        <b-nav-item :href="$config.get('helpLink')">
          <truck-icon class="mr-3" />
          {{ $t('userProfileDropdownMenu.help') }}
        </b-nav-item>
        <b-nav-item :to="languageRoute" exact :class="{ 'font-weight-bold': title === languageTitle }">
          <globe-icon class="mr-3" />
          {{ languageTitle + ' (' + $i18n.locale.toUpperCase() + ')' }}
        </b-nav-item>
        <b-nav-item :href="$config.get('logoutUrl')">
          <log-out-icon class="mr-3" />
          {{ $t('userProfileDropdownMenu.logOut') }}
        </b-nav-item>
      </template>
    </app-sidebar>
    <div class="user-retrieve__container flex-grow-1">
      <app-header hide-nav hide-search />
      <div class="container-fluid">
        <page-header :title="title" :icon="icon" class="mb-5" />
        <app-waiter :loader="fetchUserLoader" waiter-class="my-5 mx-auto d-block">
          <router-view :class="{ 'px-5': title === languageTitle }" />
        </app-waiter>
      </div>
    </div>
  </div>
</template>
