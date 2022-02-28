
<script>
import { noop } from 'lodash'
import HistoryFetcher from '@/components/HistoryFetcher'
import HistoryList from '@/components/HistoryList'

export default {
  name: 'UserRetrieveHistory',
  components: {
    HistoryFetcher,
    HistoryList
  },
  props: {
    username: {
      type: String
    }
  },
  computed: {
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
    }
  }
}
</script>

<template>
  <history-fetcher
    class="user-retrieve-history"
    :username="username"
    :page-number="pageNumber"
    :page-size="pageSize"
    #default="{ actionIds, isFetching, count }"
  >
    <history-list :fetching="isFetching" :action-ids="actionIds" >
      <template #header>
        <custom-pagination
          compact
          v-if="count > pageSize"
          v-model="pageNumber"
          :per-page="pageSize"
          :total-rows="count"
        />
      </template>
    </history-list>
  </history-fetcher>
</template>
