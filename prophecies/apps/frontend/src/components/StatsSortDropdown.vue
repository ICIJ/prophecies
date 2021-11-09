<template>
<div class="stats-sort-dropdown">
    <label>
        Sort by
      </label>
      <multiselect :allow-empty="false"
                   :show-labels="false"
                   :searchable="false"
                   :options="sortOptions"
                   :value="selectedSortOption"
                   @input="intermediarySort = $event.value"
                   label="label"
                   track-by="value" />
</div>
</template>

<script>
import { find } from 'lodash'

import Multiselect from 'vue-multiselect'

export default {
  name: 'StatsSortDropdown',
  components: {
    Multiselect
  },
  props: {
    sort: {
      type: String,
      default: 'task_id'
    }
  },
  data () {
    return {
      intermediarySort: this.sort
    }
  },
  computed: {
    sortOptions () {
      return [
        { value: 'task_id', label: 'ID (default)', $isDefault: true },
        { value: 'task_created_at_desc', label: 'Latest created' },
        { value: 'task_created_at_asc', label: 'Oldest created' }
        //   { value: 'task_record__id', label: 'Task name (A-Z)' },
        //   { value: 'task_record__id', label: 'Task name (Z-A)' },
        //   { value: 'task_record__id', label: 'Project name (A-Z)' },
        //   { value: 'task_record__id', label: 'Project name (Z-A)' },
        //   { value: 'task_record__id', label: 'Progress (low to high)' },
        //   { value: 'task_record__id', label: 'Progress (high to low)' },
        //   { value: 'task_record__priority', label: 'Priority (low to high)' },
        //   { value: '-task_record__priority', label: 'Priority (high to low)' },
      ]
    },

    selectedSortOption () {
      return find(this.sortOptions, { value: this.intermediarySort })
    }
  },
  watch: {
    sort (value) {
      this.intermediarySort = value
    }
  }
}
</script>
