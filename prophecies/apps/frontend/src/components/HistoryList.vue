<script>
import { uniqueId } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import Action from '@/models/Action'
import Task from '@/models/Task'
import Tip from '@/models/Tip'
import HistoryListGroup from '@/components/HistoryListGroup.vue'
import { ITEM_TYPES } from '@/components/HistoryListItem.vue'
const pontus = { projectId: '1', projectName: 'Pontus', tasks: [{ taskId: '2', taskName: 'Passports' }] }
const chronos = { projectId: '2', projectName: 'Chronos', tasks: [{ taskId: '1', taskName: 'Addresses' }] }

const checkedRecords = [
  {
    type: ITEM_TYPES.CHECKED_RECORDS,
    date: '2021-09-20T11:43:15.263Z',
    user: 'Jelena',
    nbRecords: 252,
    projectName: chronos.projectName,
    taskName: chronos.tasks[0].taskName
  },

  {
    type: ITEM_TYPES.CHECKED_RECORDS,
    date: '2021-09-19T11:43:15.263Z',
    user: 'Augie',
    nbRecords: 2,
    projectName: pontus.projectName,
    taskName: pontus.tasks[0].taskName
  }

]

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
      this.checkedRecords = checkedRecords
      await Task.api().get()
      await Action.api().get()
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
     <history-list-group :limit="limit" :fluid="fluid"/>
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
