
<script>
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
  }
}
</script>

<template>
  <history-fetcher class="user-retrieve-history" :username="username" #default="{actionIds, isFetching}">
    <history-list :limit='20' :fetching="isFetching" :action-ids="actionIds"/>
  </history-fetcher>
</template>
