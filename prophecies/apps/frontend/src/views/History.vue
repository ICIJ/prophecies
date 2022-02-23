<script>
import { uniqueId } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import HistoryList from '@/components/HistoryList'
import { fetchHistoryItemsIds } from '@/utils/history'

export default {
  name: 'History',
  components: {
    AppSidebar,
    AppHeader,
    HistoryList
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
      this.itemsIds = await fetchHistoryItemsIds()
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('load-history-item-')
    },
    fetching () {
      return this.$wait.is(this.fetchHistoryLoader)
    }
  }
}

</script>

<template>
  <div class="history d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="history__container flex-grow-1">
      <app-header hide-nav />
      <div class="container-fluid p-5">
        <history-list :limit='20' :fetching="fetching" :items-ids="itemsIds">
          <template v-slot:title>
            <h1 class="font-weight-bold mb-5 history__title">
              What happened <span class="history__title--lately">lately</span>
            </h1>
          </template>
        </history-list>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
 .history {
    &__title{
      color:$primary;
      &--lately{
        color:$danger;
      }
    }
 }
</style>
