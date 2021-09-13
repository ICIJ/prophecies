<script>
  import { find } from 'lodash'
  import Task from '@/models/Task'

  export default {
    name: 'TaskRecordReviewAppliedSorting',
    props: {
      sort: {
        type: String
      }
    },
    computed: {
      sortOptions () {
        return [
          { value: 'task_record__id', label: 'ID (default)', $isDefault: true },
          { value: 'task_record__predicted_value', label: 'Sorted by: predicted value (A - Z)' },
          { value: '-task_record__predicted_value', label: 'Sorted by: predicted value (Z - A)' },
          { value: 'task_record__original_value', label: 'Sorted by: original value (A - Z)' },
          { value: '-task_record__original_value', label: 'Sorted by: original value (Z - A)' },
          { value: 'task_record__priority', label: 'Sorted by: priority (low to high)', $isDisabled: true },
          { value: '-task_record__priority', label: 'Sorted by: priority (high to low)', $isDisabled: true },
        ]
      },
      selectedSortOption () {
        return find(this.sortOptions, { value: this.sort })
      },
      defaultSortOption () {
        return find(this.sortOptions, { $isDefault: true })
      },
      hasSorting () {
        return  this.sort !== this.defaultSortOption.value
      }
    },
    methods: {
      deleteSortOption (option) {
        this.$emit('update:sort', option)
      }
    }
  }
</script>

<template lang="html">
  <div class="task-record-review-applied-sort mb-4">
    <b-btn variant="default" class="task-record-review-applied-sort__item" :title="selectedSortOption['label']"  v-b-tooltip.hover @click="deleteSortOption(selectedSortOption['value'])" v-if="hasSorting">
      {{ selectedSortOption['label'] }} <x-icon class="ml-3" size="1x" />
    </b-btn>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-applied-sort {
    &__item {
      font-weight: bold;
      text-decoration: underline;
      padding-left: $spacer;
      padding-right: $spacer;
      margin-right: $spacer;
    }
  }
</style>
