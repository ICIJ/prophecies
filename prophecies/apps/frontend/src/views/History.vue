<script>
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import HistoryList from '@/components/HistoryList'
import HistoryFetcher from '@/components/HistoryFetcher'

export default {
  name: 'History',
  components: {
    AppSidebar,
    AppHeader,
    HistoryList,
    HistoryFetcher
  },
  computed: {
    pageSize() {
      return 50
    },
    pageNumber: {
      get() {
        return Number(this.$route.query['page[number]']) || 1
      },
      set(pageNumber) {
        const query = { ...this.$route.query, 'page[number]': pageNumber }
        this.$router.push({ path: this.$route.path, query }, undefined)
      }
    }
  }
}
</script>

<template>
  <div class="history d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="history__container flex-grow-1">
      <app-header hide-nav />
      <history-fetcher
        v-slot="{ actionIds, isFetching, count }"
        class="container-fluid p-5"
        :page-size="pageSize"
        :page-number="pageNumber"
      >
        <history-list :fetching="isFetching" :action-ids="actionIds">
          <template #title>
            <h1 class="font-weight-bold mb-5 history__title">
              What happened <span class="history__title--lately text-danger">lately</span>
            </h1>
          </template>
          <template #header>
            <custom-pagination
              v-if="count > pageSize"
              v-model="pageNumber"
              compact
              :per-page="pageSize"
              :total-rows="count"
            />
          </template>
        </history-list>
      </history-fetcher>
    </div>
  </div>
</template>
