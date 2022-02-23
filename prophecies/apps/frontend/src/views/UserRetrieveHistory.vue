
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
  <history-fetcher class="user-retrieve-history" :username="username" #default="{itemIds, isFetching}">
    <history-list :limit='20' :fetching="isFetching" :items-ids="itemIds"/>
  </history-fetcher>
</template>
