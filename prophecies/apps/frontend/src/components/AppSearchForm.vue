<script>
import { filter, flatten, get, maxBy, throttle, uniqueId } from 'lodash'
import { directive as onClickaway } from 'vue-clickaway'

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
    },
    searchInputSelector: {
      type: String,
      default: '.app-search-form__field__input'
    }
  },
  directives: {
    onClickaway
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
      queryset: [],
      activeItem: -1,
      activeQuerysetId: null
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
        'app-search-form--has-active-item': this.hasActiveItem,
        'app-search-form--has-query': this.hasQuery,
        'app-search-form--has-queryset': this.hasQueryset,
        'app-search-form--is-loading': this.isLoading
      }
    },
    hasActiveItem () {
      return this.activeItem > -1 && this.activeQuerysetId
    },
    hasQuery () {
      return this.query !== ''
    },
    hasQueryset () {
      return !!this.queryset.length
    },
    searchMethods () {
      return [this.searchTips, ...this.searchTaskRecordReviewMethodsByTask]
    },
    searchTaskRecordReviewMethodsByTask () {
      // Create one method for each task with at least 1 record
      return Task.query()
        .where('taskRecordsCount', (value) => { return value > 0 })
        .get()
        .map(({ id: taskId }) => {
          return (query, querysetId) => {
            return this.searchTaskRecordReview(query, querysetId, taskId)
          }
        })
    },
    shortkeys () {
      return {
        'activatePreviousItem': 'up',
        'activateNextItem': 'down',
        'close': 'esc',
        'focus': 'ctrl+f'
      }
    },
    tipsToSearch () {
      // Create tips : general tips (no task associated) and tips
      // associated to a task that has at least 1 taskRecordsCount
      return Tip.query()
        .with('task')
        .get()
        .filter(elem => elem.taskId === null || elem.task?.taskRecordsCount > 0)
        .map(({ id: tipId }) => tipId)
    },
    tipSearchParams () {
      return this.tipsToSearch.length ? { 'filter[id__in]': this.tipsToSearch.join(',') } : {}
    },
    defaultQuerysetId () {
      const maxCount = maxBy(this.counts, 'count')
      return get(maxCount, 'querysetId', null)
    },
    activeQueryset () {
      return filter(this.queryset, { querysetId: this.activeQuerysetId })
    },
    maxActiveItem () {
      return this.activeQueryset.length - 1
    }
  },
  methods: {
    close () {
      this.activeItem = -1
      this.$el.querySelector(this.searchInputSelector).blur()
    },
    focus () {
      this.$el.querySelector(this.searchInputSelector).focus()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    mapShortkeys ({ detail: { srcKey: method } }) {
      if (method in this.$options.methods) {
        this[method]()
      }
    },
    activatePreviousItem () {
      this.activeItem = Math.max(-1, this.activeItem - 1)
      // Move back to the search input
      if (this.activeItem === -1) {
        this.$el.querySelector(this.searchInputSelector).focus()
      }
    },
    activateNextItem () {
      this.activeItem = Math.min(this.maxActiveItem, this.activeItem + 1)
    },
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
    callSearchMethods (query) {
      return this.searchMethods.map(method => {
        // Each method creates a unique id
        const querysetId = uniqueId('qs-')
        return method(query, querysetId)
      })
    },
    async searchTaskRecordReview (query, querysetId, taskId) {
      const params = { 'filter[taskRecord.task]': taskId }
      const results = await TaskRecordReview.api().search(query, { params })
      const entitiesIdAndType = this.collectEntitiesIdAndType(results, querysetId)
      const count = this.collectCount(results, querysetId)
      return { entitiesIdAndType, count }
    },
    async searchTips (query, querysetId) {
      const results = await Tip.api().search(query, { params: this.tipSearchParams })
      const entitiesIdAndType = this.collectEntitiesIdAndType(results, querysetId)
      const count = this.collectCount(results, querysetId)
      return { entitiesIdAndType, count }
    },
    async search (query) {
      if (!this.isQueryValid(query)) {
        return this.emptyResultsAndCounts()
      }
      this.$wait.start(`app-search-form-load-${query}`)
      try {
        // We can search the query through several methods
        const promises = this.callSearchMethods(query)
        // Wait for all promises to be resolved
        const all = await Promise.all(promises)
        // Avoid updating component's data if the query is not current anymore
        if (this.query === query) {
          // Merge values at once
          this.counts = all.map(qs => qs.count)
          this.queryset = flatten(all.map(qs => qs.entitiesIdAndType))
          this.activeQuerysetId = this.defaultQuerysetId
          this.activeItem = -1
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
  <component
    class="app-search-form"
    v-on-clickaway="close"
    :is="is"
    :class="classList"
    @submit.prevent>
    <label 
      class="app-search-form__field d-flex align-items-center justify-content-start w-100"
      v-shortkey="shortkeys"
      @shortkey="mapShortkeys($event)">
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
        @input="searchWithThrottle(query)"
        @keyup.up="activatePreviousItem"
        @keyup.down="activateNextItem"
        @keyup.esc="close"
        class="app-search-form__field__input flex-grow-1"
        placeholder="Type your search"
        type="search"
        v-model="query" />
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
        :active-item.sync="activeItem"
        :active-queryset-id.sync="activeQuerysetId"
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
      .app-search-form--has-active-item &__placeholder,
      &__input:focus ~ &__placeholder {
        display: none;
      }

      .app-search-form--has-query &__separator,
      .app-search-form--has-active-item &__separator,
      &__input:focus ~ &__separator {
        display: block;
      }

      .app-search-form--has-queryset &__input:focus ~ &__results,
      .app-search-form--has-active-item &__results,
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
