<script>
  import { find } from 'lodash'
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
    computed: {
      pageSizeOptions () {
        return [
          { value: '10', label: '10 by page' },
          { value: '25', label: '25 by page' },
          { value: '50', label: '50 by page' }
        ]
      },
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
      selectedPageSizeOption () {
        return find(this.pageSizeOptions, { value: this.pageSize })
      },
      selectedSortOption () {
        return find(this.sortOptions, { value: this.sort })
      },
      isDefaultSortOption () {
        return this.sort === this.$options.props.sort.default
      }
    }
  }
</script>

<template>
  <div class="task-record-review-page-params d-inline-flex">
    <div class="task-record-review-page-params__size pr-3">
      <multiselect :allow-empty="false"
                   :show-labels="false"
                   :searchable="false"
                   :options="pageSizeOptions"
                   :value="selectedPageSizeOption"
                   @input="$emit('update:pageSize', $event.value)"
                   label="label"
                   track-by="value" />
    </div>
    <div class="task-record-review-page-params__sort" :class="{ 'task-record-review-page-params__sort--default': isDefaultSortOption }">
      <multiselect :allow-empty="false"
                   :show-labels="false"
                   :searchable="false"
                   :options="sortOptions"
                   :value="selectedSortOption"
                   @input="$emit('update:sort', $event.value)"
                   label="label"
                   track-by="value" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-page-params {

    /deep/ .multiselect {
      min-height: 0;

      &__tags {
        font-size: 1rem;
        min-height: 0;
        padding-top: 7px;
      }

      &__single, &__placeholder {
        padding-top: 0;
        margin: 0;
        font-size: 1rem;
        min-height: 25px;
      }

      &__select {
        height: 33px;
      }
    }

    &__size {
      min-width: 200px;
    }

    &__sort {
      min-width: 250px;
    }
  }
</style>
