<script>
  import { find } from 'lodash'
  import Task from '@/models/Task'

  export default {
    name: 'TaskRecordReviewAppliedSorting',
    props: {
      sort: {
        type: String
      },
      hasSorting: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      sortOptions () {
        return [
          { value: 'task_record__id', label: 'ID (default)', $isDefault: true },
          { value: 'task_record__predicted_value', label: 'Predicted value (A - Z)' },
          { value: '-task_record__predicted_value', label: 'Predicted value (Z - A)' },
          { value: 'task_record__original_value', label: 'Original value (A - Z)' },
          { value: '-task_record__original_value', label: 'Original value (Z - A)' },
          { value: 'task_record__priority', label: 'Priority (low to high)', $isDisabled: true },
          { value: '-task_record__priority', label: 'Priority (high to low)', $isDisabled: true },
        ]
      },
      selectedSortOption () {
        return find(this.sortOptions, { value: this.sort })
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
    <b-btn variant="primary" class="task-record-review-applied-sort__item" :title="selectedSortOption['label']"  v-b-tooltip.hover @click="deleteSortOption(selectedSortOption['value'])" v-if="hasSorting">
      {{ selectedSortOption['label'] }} <x-icon class="ml-3" size="1x" />
    </b-btn>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-applied-sort {
    &__item {
      font-weight: bold;
      padding-left: $spacer;
      padding-right: $spacer;
      margin-right: $spacer;
    }

    & /deep/ &__item.btn:hover {
      background-color: $warning;
      border-color: $warning;
      color: text-contrast($warning);
    }
  }
</style>
