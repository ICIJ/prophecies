<script>
import { get, noop, uniqueId } from 'lodash'
import UserNotifications from '@/components/UserNotifications'
import UserNotification from '@/models/UserNotification'

export default {
  name: 'UserRetrieveNotifications',
  components: {
    UserNotifications
  },
  data () {
    return {
      count: 0,
      notificationIds: []
    }
  },
  created () {
    return this.fetchWithLoader()
  },
  watch: {
    pageNumber () {
      return this.fetchWithLoader()
    }
  },
  computed: {
    loader () {
      return uniqueId('user-retrieve-notifications-')
    },
    fetching () {
      return this.$wait.is(this.loader)
    },
    pageSize () {
      return 50
    },
    pageNumber: {
      get () {
        return Number(this.$route.query['page[number]']) || 1
      },
      set (pageNumber) {
        const query = { ...this.$route.query, 'page[number]': pageNumber }
        this.$router.push({ path: this.$route.path, query }, noop)
      }
    },
    showPagination () {
      return !this.fetching && this.count > this.pageSize
    }
  },
  methods: {
    async fetch () {
      const pageSize = this.pageSize
      const pageNumber = this.pageNumber
      const include = 'action.actionObject'
      const params = { 'page[size]': pageSize, 'page[number]': pageNumber, include }
      try {
        // This populates the store automaticaly with Vuex ORM
        const { response } = await UserNotification.api().get('', { params })
        // Collect fetched ids
        this.notificationIds = get(response, 'data.data', []).map(n => n.id)
        this.count = get(response, 'data.meta.pagination.count', 0)
      } catch (error) {
        this.$router.replace({ name: 'error', params: { error } })
      }
    },
    async fetchWithLoader () {
      this.$wait.start(this.loader)
      await this.fetch()
      this.$wait.end(this.loader)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-notifications">
    <user-notifications :notification-ids="notificationIds" :fetching="fetching" />
    <custom-pagination
      compact
      v-if="showPagination"
      v-model="pageNumber"
      :per-page="pageSize"
      :total-rows="count" />
  </div>
</template>

<style lang="scss">
  .user-retrieve-notifications {
    .user-notification-link:hover {
      text-decoration: none;
      color: $dropdown-link-hover-color;
      background: $dropdown-link-hover-bg;
    }
  }
</style>
