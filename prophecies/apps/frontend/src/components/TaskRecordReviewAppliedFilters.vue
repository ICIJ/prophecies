<script>
  import { find, mapValues, reduce, without } from 'lodash'
  import taskRecordReviewFiltersMixin from '@/mixins/task-record-review-filters'
  import Task from '@/models/Task'

  export default {
    name: 'TaskRecordReviewAppliedFilters',
    mixins: [taskRecordReviewFiltersMixin],
    props: {
      taskId: {
        type: [String, Number]
      },
      routeFilters: {
        type: Object,
        default: () => ({})
      }
    },
    computed: {
      filters () {
        const filters = this.getTaskFilters(this.task)
        const selectedOptions = this.mapRouteQueryToFilterOptions(this.routeFilters, this.task)
        // Merge the filter object with the corresponding selected options
        return mapValues(filters, (filter, key) => {
          const [, selected] = find(selectedOptions, entry =>entry[0] === key) || []
          filter.selected = selected || []
          return filter
        })
      },
      task () {
        return Task
          .query()
          .with('checkers')
          .with('choiceGroup')
          .with('choiceGroup.alternativeValues')
          .with('choiceGroup.choices')
          .find(this.taskId)
      },
    },
    methods: {
      deleteFilterOption (filter, option) {
        const selected = mapValues(this.filters, ({ name, selected }) => {
          if (filter.name === name) {
            return without(selected, option)
          }
          return selected
        })
        const routeFilters = this.getSelectedFiltersAsQueryParams(this.filters, selected)
        /**
         * @event update:routeFilters
         * @param routes query params after deleting an option
         */
        this.$emit('update:routeFilters', routeFilters)
      }
    }
  }
</script>

<template>
  <div class="task-record-review-applied-filters mb-4">
    <template v-for="filter of filters">
      <template v-for="option in filter.selected">
        <b-btn variant="primary" class="task-record-review-applied-filters__item" :title="filter.name"  v-b-tooltip.hover @click="deleteFilterOption(filter, option)">
          {{ option[filter.label || 'name'] }}<x-icon class="ml-3" size="1x" />
        </b-btn>
      </template>
    </template>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-applied-filters {
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
