<script>
import { uniqueId } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import HistoryList from '@/components/HistoryList'
import Task from '@/models/Task'
import Action from '@/models/Action'
import ActionAggregate from '@/models/ActionAggregate'
import Tip from '@/models/Tip'

const getIds = (object) => {
  const { response: { data: { data: arr } } } = object
  return arr.map(o => o.id)
}

export const fetchHistoryItemsIds = async (userId) => {
  const taskIdParams = userId ? { 'filter[checkers]': userId } : null
  const actionIdParams = { 'filter[verb]': 'mentioned' }
  const actionAggregateIdParams = userId ? { 'filter[user]': userId } : null
  const tipIdParams = userId ? { 'filter[creator]': userId } : null

  const taskPromise = Task.api().get('', {params: taskIdParams})
    .then(response => getIds(response))
  const actionPromise = Action.api().get('', { params: actionIdParams })
    .then(({ response:{data:{data : actions}} }) => {
      if ( userId ) {
        actions = actions.filter(({ relationships: {actor, target}}) => {
          return actor.data.id === userId || target.data.id === userId
        })
      }
      return actions.map(action => action.id)
    });
  const actionAggregatePromise = ActionAggregate.api().get('', { params: actionAggregateIdParams })
    .then(response => getIds(response));
  const tipPromise = Tip.api().get('', { params: tipIdParams })
    .then(response => getIds(response));
  const [taskIds , actionIds, actionAggregateIds, tipIds] = await Promise.all([
    taskPromise,
    actionPromise,
    actionAggregatePromise,
    tipPromise
  ])
  return { taskIds , actionIds, actionAggregateIds, tipIds }
}

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
