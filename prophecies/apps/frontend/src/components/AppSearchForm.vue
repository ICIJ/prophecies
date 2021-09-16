<script>
import { get, throttle } from 'lodash'
import AppSearchResults from '@/components/AppSearchResults'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  props: {
    isNav: {
      type: Boolean
    }
  },
  components: {
    AppSearchResults,
    ShortkeyBadge
  },
  data () {
    return {
      query: '',
      results: []
    }
  },
  watch: {
    query () {
      return this.searchWithThrottle(this.query)
    }
  },
  computed: {
    is () {
      return this.isNav ? 'b-nav-form' : 'form'
    },
    classList () {
      return {
        'app-search-form--has-query': this.hasQuery,
        'app-search-form--has-results': this.hasResults,
      }
    },
    hasQuery () {
      return this.query !== ''
    },
    hasResults () {
      return !!this.results.length
    }
  },
  methods: {
    collectEntitiesIdAndType (results = []) {
      const data = get(results, 'response.data.data', [])
      return data.map(({ id, type }) => ({ id, type }))
    },
    async searchTaskRecordReview (query) {
      const results = await TaskRecordReview.api().search(query)
      return this.collectEntitiesIdAndType(results)
    },
    async search (query) {
      this.results = !query ? [] : [ ...await this.searchTaskRecordReview(query) ]
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
      <search-icon class="mr-2 app-search-form__field__icon" />
      <b-form-input
        v-model="query"
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
        :query="query"
        :results="results"
        class="app-search-form__field__results" />
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

      &__icon {
        height: 20px;
        width: 20px
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

      .app-search-form--has-results &__input:focus ~ &__results,
      .app-search-form--has-results &__results:hover {
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
