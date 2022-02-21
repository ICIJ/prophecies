<script>
import {get, uniqueId} from 'lodash'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import HistoryList from '@/components/HistoryList'
import Task from '@/models/Task'
import Action from '@/models/Action'
import ActionAggregate from '@/models/ActionAggregate'
import Tip from '@/models/Tip'

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
      this.itemsIds.taskIds = get(await Task.api().get(), 'response.data.data', []).map(t => t.id)
      this.itemsIds.actionIds = get(await Action.api().get(), 'response.data.data', []).map(a => a.id)
      this.itemsIds.actionAggregateIds = get(await ActionAggregate.api().get(), 'response.data.data', []).map(aa => aa.id)
      this.itemsIds.tipIds = get(await Tip.api().get(), 'response.data.data', []).map(t => t.id)
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
