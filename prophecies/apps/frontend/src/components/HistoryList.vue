<script>
import {uniqueId} from 'lodash'
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
    },
    fetching: {
      type: Boolean
    },
    itemsIds: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      more: 5,
      nbTimesMore: 0,
      checkedRecords: []
    }
  },
  created () {
    if (this.fetching) {
      this.$wait.start(this.loader)
    }
  },
  watch: {
    fetching (fetching) {
      if (!fetching) {
        this.$wait.end(this.loader)
      }
    }
  },
  computed: {
    loader () {
      return uniqueId('load-history-list-item-')
    },
    tasks () {
      return Task
        .query()
        .whereIdIn(this.taskIds)
        .get()
    },
    actions () {
      return Action
        .query()
        .whereIdIn(this.actionIds)
        .get()
    },
    actionAggregates () {
      return ActionAggregate
        .query()
        .whereIdIn(this.actionAggregateIds)
        .get()
    },
    tips () {
      return Tip
        .query()
        .whereIdIn(this.tipIds)
        .get()
    },
    hasTitleSlot() {
      return !!this.$slots.title
    }
  }
}
</script>

<template>
    <app-waiter :loader="loader" waiter-class="my-5 mx-auto d-block">
    <h1 class="font-weight-bold mt-3 mb-5 history-list__title" v-if="hasTitleSlot">
      <slot name="title">
        What happened <span class="text-danger">lately</span>
      </slot>
    </h1>
     <history-list-group :limit="limit" :fluid="fluid" :items-ids="itemsIds">
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
