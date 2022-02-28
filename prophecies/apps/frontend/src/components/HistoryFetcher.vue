
<script>
import { get, uniqueId } from 'lodash'
import { fetchHistoryItemsIds } from '@/utils/history'
import User from '@/models/User'

export default {
  name: 'HistoryFetcher',
  props: {
    username: {
      type: String,
      default: null
    },
    pageSize: {
      type: Number,
      default: null
    },
    pageNumber: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      isFetching: false,
      actionIds: [],
      count: 0
    }
  },
  async created () {
    await this.setup()
  },
  methods: {
    async setup () {
      try {
        this.isFetching = true
        await this.fetchAll()
      } catch (error) {
        const title = 'Unable to retrieve history'
        this.$router.replace({ name: 'error', params: { title, error } })
      } finally {
        this.isFetching = false
      }
    },
    async fetchAll () {
      if (this.username && !this.user?.id) {
        return Promise.reject(new Error('User not found'))
      }
      const { response } = await fetchHistoryItemsIds(this.user?.id, this.pageSize, this.pageNumber)
      this.actionIds = get(response, 'data.data', []).map(a => a.id)
      this.count = get(response, 'data.meta.pagination.count', 0)
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('fetch-history-')
    },
    user () {
      return User.find(this.username)
    }
  },
  watch: {
    pageNumber (value) {
      return this.setup()
    }
  }
}
</script>

<template>
  <div class="history-fetcher">
    <slot v-bind="{ actionIds, isFetching, count }"/>
  </div>
</template>
