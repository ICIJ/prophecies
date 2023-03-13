<script>
import {find} from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'TaskRecordReviewPageParams',
  components: {
    Multiselect
  },
  props: {
    pageSize: {
      type: String,
      default: '10'
    },
    sort: {
      type: String,
      default: 'task_record__id'
    }
  },
  data() {
    return {
      intermediaryPageSize: this.pageSize,
      intermediarySort: this.sort
    }
  },
  watch: {
    pageSize(value) {
      this.intermediaryPageSize = value
    },
    sort(value) {
      this.intermediarySort = value
    }
  },
  computed: {
    pageSizeOptions() {
      return [
        {value: '10', label: '10 by page'},
        {value: '25', label: '25 by page'},
        {value: '50', label: '50 by page'}
      ]
    },
    sortOptions() {
      return [
        {value: 'task_record__id', label: this.$t('taskRecordReviewPageParams.idDefault'), $isDefault: true},
        {value: 'task_record__predicted_value', label: this.$t('taskRecordReviewPageParams.predictedValueAZ')},
        {value: '-task_record__predicted_value', label: this.$t('taskRecordReviewPageParams.predictedValueZA')},
        {value: 'task_record__original_value', label: this.$t('taskRecordReviewPageParams.originalValueAZ')},
        {value: '-task_record__original_value', label: this.$t('taskRecordReviewPageParams.originalValueZA')},
        {
          value: 'task_record__priority',
          label: this.$t('taskRecordReviewPageParams.priorityValueLowHigh'),
          $isDisabled: true
        },
        {
          value: '-task_record__priority',
          label: this.$t('taskRecordReviewPageParams.priorityValueHighLow'),
          $isDisabled: true
        }
      ]
    },
    selectedPageSizeOption() {
      return find(this.pageSizeOptions, {value: this.intermediaryPageSize})
    },
    selectedSortOption() {
      return find(this.sortOptions, {value: this.intermediarySort})
    },
    isDefaultSortOption() {
      return this.intermediarySort === this.$options.props.sort.default
    }
  },
  methods: {
    submit() {
      const pageSize = this.intermediaryPageSize
      const sort = this.intermediarySort
      this.$emit('submit', {pageSize, sort})
    }
  }
}
</script>

<template>
  <form class="task-record-review-page-params" @submit.prevent="submit">
    <div class="task-record-review-page-params__size task-record-review-page-params__form-group">
      <label class="task-record-review-page-params__form-group__label">
        {{ $t('taskRecordReviewPageParams.pageSize')}}
      </label>
      <multiselect :allow-empty="false"
                   :show-labels="false"
                   :searchable="false"
                   :options="pageSizeOptions"
                   :value="selectedPageSizeOption"
                   @input="intermediaryPageSize = $event.value"
                   label="label"
                   track-by="value"/>
    </div>
    <div class="task-record-review-page-params__sort task-record-review-page-params__form-group"
         :class="{ 'task-record-review-page-params__sort--default': isDefaultSortOption }">
      <label class="task-record-review-page-params__form-group__label">
        {{$t('taskRecordReviewPageParams.sortBy')}}
      </label>
      <multiselect :allow-empty="false"
                   :show-labels="false"
                   :searchable="false"
                   :options="sortOptions"
                   :value="selectedSortOption"
                   @input="intermediarySort = $event.value"
                   label="label"
                   track-by="value"/>
    </div>
    <div class="d-flex pt-2">
      <b-button @click="$emit('cancel')" variant="secondary">
        Cancel
      </b-button>
      <b-button variant="primary" class="ml-auto font-weight-bold" type="submit">
        Apply
      </b-button>
    </div>
  </form>
</template>

<style lang="scss" scoped>
.task-record-review-page-params {

  &__form-group {
    display: block;
    margin-bottom: $spacer;

    &__label {
      font-weight: bold;
    }
  }
}
</style>
