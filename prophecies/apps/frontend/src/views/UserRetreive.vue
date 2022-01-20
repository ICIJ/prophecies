<script>
import { camelCase, uniqueId } from 'lodash'

import User from '@/models/User'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import PageHeader from '@/components/PageHeader'

export default {
  name: 'UserRetreive',
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
  async created () {
    await this.fetchUserWithLoader()
  },
  computed: {
    routeKey () {
      return camelCase(this.$route.name)
    },
    routeTitleKey () {
      if (this.user?.isMe) {
        return [this.routeKey, 'title', 'yours'].join('.')
      }
      return [this.routeKey, 'title', 'others'].join('.')
    },
    userRoute () {
      const params = { username: this.username }
      return { name: 'user-retreive', params }
    },
    fetchUserLoader () {
      return uniqueId('load-user-')
    },
    title () {
      return this.$t(this.routeTitleKey, this.user)
    },
    user () {
      return User.query().where('username', this.username).first()
    },
    icon () {
      return 'UserIcon'
    }
  },
  methods: {
    fetchUser () {
      return User.api().get(this.username)
    },
    async fetchUserWithLoader () {
      this.$wait.start(this.fetchUserLoader)
      await this.fetchUser()
      this.$wait.end(this.fetchUserLoader)
    }
  },
  watch: {
    title () {
      if (this.user) {
        this.$core.setPageTitle(this.title)
      }
    },
    async username () {
      await this.fetchUserWithLoader()
    }
  }
}
</script>

<template>
  <div class="user-retreive d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top">
      <template #items>
        <b-nav-item :to="userRoute" exact>
          <user-icon class="mr-3" />
          Profile
        </b-nav-item>
        <b-nav-item :href="$config.get('helpLink')">
          <truck-icon class="mr-3" />
          Help
        </b-nav-item>
        <b-nav-item :href="$config.get('logoutUrl')">
          <log-out-icon class="mr-3" />
          Sign out
        </b-nav-item>
      </template>
    </app-sidebar>
    <div class="user-retreive__container flex-grow-1">
      <app-header hide-nav hide-search />
      <div class="container-fluid">
        <page-header :title="title" :icon="icon" class="mb-5" />
        <app-waiter :loader="fetchUserLoader" waiter-class="my-5 mx-auto d-block">
          <router-view />
        </app-waiter>
      </div>
    </div>
  </div>
</template>