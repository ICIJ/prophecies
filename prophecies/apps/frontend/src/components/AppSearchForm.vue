<script>
import { flatten, get, throttle, uniqueId } from 'lodash'
import AppSearchResults from '@/components/AppSearchResults'
import AppWaiter from '@/components/AppWaiter'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import Tip from '@/models/Tip'

export default {
  props: {
    isNav: {
      type: Boolean
    }
  },
  components: {
    AppSearchResults,
    AppWaiter,
    ShortkeyBadge
  },
  data () {
    return {
      counts: [],
      query: '',
      queryset: []
    }
  },
  computed: {
    is () {
      return this.isNav ? 'b-nav-form' : 'form'
    },
    isLoading () {
      return this.$wait.is(`app-search-form-load-${this.query}`)
    },
    classList () {
      return {
        'app-search-form--has-query': this.hasQuery,
        'app-search-form--has-queryset': this.hasQueryset,
        'app-search-form--is-loading': this.isLoading,
      }
    },
    hasQuery () {
      return this.query !== ''
    },
    hasQueryset () {
      return !!this.queryset.length
    },
    searchMethods () {
      return [ this.searchTips, ...this.searchTaskRecordReviewMethodsByTask ]
    },
    searchTaskRecordReviewMethodsByTask () {
      // Create one method for each task
      return Task.all().map(({ id: taskId }) => {
        return (query, querysetId) => {
          return this.searchTaskRecordReview(query, querysetId, taskId)
        }
      })
    }
  },
  methods: {
    collectEntitiesIdAndType ({ response }, querysetId) {
      const data = get(response, 'data.data', [])
      return data.map(({ id, type }) => ({ id, type, querysetId }))
    },
    collectCount ({ response }, querysetId) {
      const cannocialCount = get(response, 'data.data.length', 0)
      const count = get(response, 'data.meta.pagination.count', cannocialCount)
      return { count, querysetId }
    },
    emptyResultsAndCounts () {
      this.counts = []
      this.queryset = []
    },
    isQueryValid (query) {
      return String(query).length > 1
    },
    async searchTaskRecordReview (query, querysetId, taskId) {
      const params = { 'filter[taskRecord.task]': taskId }
      const results = await TaskRecordReview.api().search(query, { params })
      const entitiesIdAndType = this.collectEntitiesIdAndType(results, querysetId)
      const count = this.collectCount(results, querysetId)
      return { entitiesIdAndType, count }
    },
    async searchTips (query, querysetId) {
      const results = await Tip.api().search(query)
      const entitiesIdAndType = this.collectEntitiesIdAndType(results, querysetId)
      const count = this.collectCount(results, querysetId)
      return { entitiesIdAndType, count }
    },
    async search (query) {
      if (!this.isQueryValid(query)) {
        return this.emptyResultsAndCounts()
      }
      this.$wait.start(`app-search-form-load-${query}`)
      // We can search the query through several methods
      const querysetId = uniqueId('queryset-')
      const promises = this.searchMethods.map(method => method(query, querysetId))
      try {
        const all = await Promise.all(promises)
        // Avoid updating component's data if the query is not current anymore
        if (this.query === query) {
          // Merge values at once
          this.counts = all.map(qs => qs.count)
          this.queryset = flatten(all.map(qs => qs.entitiesIdAndType))
        }
      } finally {
        this.$wait.end(`app-search-form-load-${query}`)
      }
    },
    searchWithThrottle: throttle(function (query) {
      return this.search(query)
    }, 600)
  }
}
</script>

<template>
  <component :is="is" class="app-search-form" :class="classList" @submit.prevent>
    <label class="app-search-form__field d-flex align-items-center justify-content-start w-100">
      <app-waiter
        :loader="`app-search-form-load-${query}`"
        :transition="null"
        :waiter-class="null"
        class="app-search-form__field__waiter mr-2"
        small
        variant="primary">
        <search-icon class="app-search-form__field__waiter__icon" />
      </app-waiter>
      <b-form-input
        v-model="query"
        @input="searchWithThrottle(query)"
        v-shortkey.focus="['ctrl', 'f']"
        type="search"
        placeholder="Type your search"
        class="app-search-form__field__input flex-grow-1" />
      <span class="app-search-form__field__placeholder">
        {{ $t('appHeader.search') }}
        <shortkey-badge
          :value="['Ctrl', 'f']"
          class="ml-2 app-search-form__field__input__placeholder__shortkey-badge" />
      </span>
      <span class="app-search-form__field__separator"></span>
      <app-search-results
        class="app-search-form__field__results"
        v-if="hasQueryset && !isLoading"
        :counts="counts"
        :query="query"
        :queryset="queryset" />
    </label>
  </component>
</template>


<style lang="scss" scoped>
  .app-search-form {
    position: relative;

    & > * {
      width: 100%;
    }

    &__field {
      padding: $spacer-xs;

      &__waiter {
        height: 20px;
        width: 20px;
        overflow: hidden;

        &__icon {
          height: 20px;
          width: 20px
        }
      }

      & &__input {
        padding: 0;
        border: 0;
        height: auto;
        opacity: 0;
        position: absolute;
        left: -9999px;

        .app-search-form--has-query &,
        &:focus {
          position: static;
          opacity: 1;
          outline: none;
          box-shadow: none;
        }
      }

      .app-search-form--has-query &__placeholder,
      &__input:focus ~ &__placeholder {
        display: none;
      }


      .app-search-form--has-query &__separator,
      &__input:focus ~ &__separator {
        display: block;
      }

      .app-search-form--has-queryset &__input:focus ~ &__results,
      .app-search-form--has-queryset &__results:hover {
        display: block;
      }

      &__placeholder {
        display: flex;
        align-items: center;
      }

      &__separator {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        background: $warning;
        height: 7px;
        max-width: 100px;
        width: 100%;
      }

      &__results {
        display: none;
        z-index: $zindex-dropdown;
        position: absolute;
        top: calc(100% + #{$spacer});
        left: 0;
        width: 800px;
        max-width: 60vw;
      }
    }
  }
</style>
