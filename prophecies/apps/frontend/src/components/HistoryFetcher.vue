
<script>
import { uniqueId } from 'lodash'
import { fetchHistoryItemsIds } from '@/utils/history'
import User from '@/models/User'

export default {
  name: 'HistoryFetcher',
  props: {
    username: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      actionIds: []
    }
  },
  async created () {
    await this.setup()
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchHistoryLoader, this.fetchAll)
      } catch (error) {
        const title = 'Unable to retrieve history'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    async fetchAll () {
      if (this.username && !this.user?.id) {
        return Promise.reject(new Error('User not found'))
      }
      this.actionIds = await fetchHistoryItemsIds(this.user?.id)
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('fetch-history-')
    },
    isFetching () {
      return this.$wait.is(this.fetchHistoryLoader)
    },
    user () {
      return User.find(this.username)
    }
  }
}
</script>

<template>
  <div class="history-fetcher">
    <slot v-bind="{actionIds,isFetching}"/>
  </div>
</template>
