<script>
import { uniqueId } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import Action from '@/models/Action'
import Task from '@/models/Task'
import Tip from '@/models/Tip'
import ActionAggregate from '@/models/ActionAggregate'
import HistoryListGroup from '@/components/HistoryListGroup.vue'

export default {
  name: 'HistoryList',
  components: {
    AppWaiter,
    HistoryListGroup
  },
  props: {
    limit: {
      type: Number,
      default: -1
    },
    fluid: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      more: 5,
      nbTimesMore: 0,
      checkedRecords: []
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
      await Task.api().get()
      await Action.api().get()
      await ActionAggregate.api().get()
      await Tip.api().get()
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('load-history-item-')
    }
  }
}
</script>

<template>
    <app-waiter :loader="fetchHistoryLoader" waiter-class="my-5 mx-auto d-block">
    <h1 class="font-weight-bold mt-3 mb-5 history-list__title"><slot name="title">What happened <span class="text-danger">lately</span></slot></h1>
     <history-list-group :limit="limit" :fluid="fluid">
       <template v-slot:footer>
       <slot name="footer"/>
       </template>
     </history-list-group>

    </app-waiter>
</template>

<style lang="scss">
 .history-list {
    &__title{
      color:$primary;
        letter-spacing: -0.03em;
    }
 }
</style>
