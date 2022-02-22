
<script>
import { uniqueId } from 'lodash'
import { fetchHistoryItemsIds } from '@/views/History'
import AppWaiter from '@/components/AppWaiter'
import HistoryList from '@/components/HistoryList'
import User from '@/models/User'

export default {
  name: "UserRetrieveHistory",
  components: {
    AppWaiter,
    HistoryList
  },
  props: {
    username: {
      type: String
    }
  },
  data () {
    return {
      itemsIds: {}
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
      this.itemsIds = await fetchHistoryItemsIds(this.user.id)
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('load-history-item-')
    },
    fetching () {
      return this.$wait.is(this.fetchHistoryLoader)
    },
    user () {
      return User.find(this.username)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-history">
    <history-list :limit='20' :fetching="fetching" :items-ids="itemsIds"/>
  </div>
</template>


<style scoped>

</style>
