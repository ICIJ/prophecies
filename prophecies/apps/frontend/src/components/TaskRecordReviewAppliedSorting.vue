<script>
import {find} from 'lodash'

export default {
  name: 'TaskRecordReviewAppliedSorting',
  props: {
    sort: {
      type: String
    }
  },
  computed: {
    sortOptions() {
      return [
        {value: 'task_record__id', label: this.$t('taskRecordReviewAppliedSorting.idDefault'), $isDefault: true},
        {value: 'task_record__predicted_value', label: this.$t('taskRecordReviewAppliedSorting.predictedValueAZ')},
        {value: '-task_record__predicted_value', label: this.$t('taskRecordReviewAppliedSorting.predictedValueZA')},
        {value: 'task_record__original_value', label: this.$t('taskRecordReviewAppliedSorting.originalValueAZ')},
        {value: '-task_record__original_value', label: this.$t('taskRecordReviewAppliedSorting.originalValueZA')},
        {
          value: 'task_record__priority',
          label: this.$t('taskRecordReviewAppliedSorting.priorityValueLowHigh'),
          $isDisabled: true
        },
        {
          value: '-task_record__priority',
          label: this.$t('taskRecordReviewAppliedSorting.priorityValueHighLow'),
          $isDisabled: true
        }
      ]
    },
    selectedSortOption() {
      return find(this.sortOptions, {value: this.sort})
    },
    defaultSortOption() {
      return find(this.sortOptions, {$isDefault: true})
    },
    hasSorting() {
      return this.sort !== this.defaultSortOption.value
    }
  },
  methods: {
    deleteSortOption(option) {
      this.$emit('update:sort', option)
    }
  }
}
</script>

<template>
  <div class="task-record-review-applied-sort">
    <b-btn variant="default" class="task-record-review-applied-sort__item" :title="selectedSortOption['label']"
           v-b-tooltip.hover @click="deleteSortOption(selectedSortOption['value'])" v-if="hasSorting">
      {{ selectedSortOption['label'] }}
      <x-icon class="ml-3" size="1x"/>
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
