<script>
import { uniqueId } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
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
    actionIds: {
      type: Array,
      default: () => ([])
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
    hasTitleSlot () {
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
     <history-list-group :limit="limit" :fluid="fluid" :action-ids="actionIds">
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
