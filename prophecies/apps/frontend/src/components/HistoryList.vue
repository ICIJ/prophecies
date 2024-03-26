<script>
import { uniqueId } from 'lodash'

import AppWaiter from '@/components/AppWaiter'
import HistoryListGroup from '@/components/HistoryListGroup'
import EmptyPlaceholder from '@/components/EmptyPlaceholder'

export default {
  name: 'HistoryList',
  components: {
    AppWaiter,
    HistoryListGroup,
    EmptyPlaceholder
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
      default: () => []
    }
  },
  data() {
    return {
      more: 5,
      nbTimesMore: 0,
      checkedRecords: [],
      useLoader: null
    }
  },
  computed: {
    loaderAll() {
      return uniqueId('load-all-history-list-')
    },
    loader() {
      return uniqueId('load-history-list-item-')
    },
    hasTitleSlot() {
      return !!this.$slots.title
    }
  },
  watch: {
    fetching: {
      immediate: true,
      handler(isFetching) {
        if (isFetching) {
          if (!this.useLoader) {
            this.useLoader = this.loaderAll
          }
          this.$wait.start(this.useLoader)
        } else {
          this.$wait.end(this.useLoader)
          if (this.useLoader === this.loaderAll) {
            this.useLoader = this.loader
          }
        }
      }
    }
  }
}
</script>

<template>
  <app-waiter :loader="loaderAll" waiter-class="my-5 mx-auto d-block" class="history-list">
    <h1 v-if="hasTitleSlot" class="font-weight-bold mt-3 mb-5 history-list__title">
      <slot name="title"> What happened <span class="text-danger">lately</span> </slot>
    </h1>
    <template v-if="actionIds.length">
      <slot name="header" />
      <app-waiter :loader="loader" waiter-class="my-5 mx-auto d-block">
        <history-list-group :limit="limit" :fluid="fluid" :action-ids="actionIds">
          <template #footer>
            <slot name="footer" />
          </template>
        </history-list-group>
      </app-waiter>
    </template>
    <slot v-else name="empty">
      <empty-placeholder :title="$t('userRetrieveHistory.noHistory')" />
    </slot>
  </app-waiter>
</template>

<style lang="scss">
.history-list {
  &__title {
    color: $primary;
    letter-spacing: -0.03em;
  }
}
</style>
