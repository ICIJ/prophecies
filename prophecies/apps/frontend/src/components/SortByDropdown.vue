<template>
    <label :for="dropdownId" class="sort-by-dropdown ">
      <slot name="label">
      </slot>
      <multiselect :allow-empty="false"
                    :show-labels="false"
                    :searchable="false"
                    :options="options"
                    :value="selectedSortOption"
                    :placeholder="$t('taskRecordReviewPageParams.sortBy')"
                    @input="intermediarySort = $event.value"
                    label="label"
                    track-by="value"
                    class="sort-by-dropdown__select "/>
    </label>
</template>

<script>
import { find, uniqueId } from 'lodash'

import Multiselect from 'vue-multiselect'

export default {
  name: 'SortByDropdown',
  components: {
    Multiselect
  },
  model: {
    prop: 'sort',
    event: 'update:sort'
  },
  props: {
    sort: {
      type: String,
      default: null
    },
    options: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      dropdownId: uniqueId('sortByDropdown-')
    }
  },
  computed: {
    selectedSortOption () {
      return find(this.options, { value: this.intermediarySort })
    },
    intermediarySort: {
      get () {
        return this.sort
      },
      set (value) {
        this.$emit('update:sort', value)
      }
    }
  }
}
</script>
