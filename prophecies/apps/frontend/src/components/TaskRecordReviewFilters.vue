<script>
  import { find, map, mapValues, trim, uniqueId } from 'lodash'
  import Multiselect from 'vue-multiselect'
  import taskRecordReviewFiltersMixin from '@/mixins/task-record-review-filters'
  import ChoiceGroup from '@/models/ChoiceGroup'
  import Task from '@/models/Task'
  import TaskRecordReview from '@/models/TaskRecordReview'

  export default {
    name: 'TaskRecordReviewFilters',
    mixins: [taskRecordReviewFiltersMixin],
    components: {
      Multiselect
    },
    props: {
      taskId: {
        type: [Number, String]
      },
      routeFilters: {
        type: Object,
        default: () => ({})
      }
    },
    data () {
      return {
        selected: {
          predictedValues: [],
          assignedTo: [],
          reviewedBy: [],
          choices: [],
        }
      }
    },
    created () {
      this.readRouteFilters()
    },
    computed: {
      filters () {
        // Method from the mixins
        return this.getTaskFilters(this.task)
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
      filtersAsQueryParams () {
        // Method from the mixins
        return this.getSelectedFiltersAsQueryParams(this.filters, this.selected)
      }
    },
    methods: {
      addArbitraryPredictedValue (value) {
        // Method from the mixins
        const option = this.toSerializableOption(value)
        this.selected.predictedValues.push(option)
      },
      readRouteFilters () {
        // Method from the mixins
        const options = this.mapRouteQueryToFilterOptions(this.routeFilters, this.task)
        // Apply the selected options to each filter
        options.forEach(([key, option]) => this.$set(this.selected, key, option))
      }
    },
    watch: {
      routeFilters: {
        deep: true,
        handler () {
          this.readRouteFilters()
        }
      },
      selected: {
        deep: true,
        handler () {
          /**
           * @event update:routeFilters
           * @param routes query params after updating filters
           */
          this.$emit('update:routeFilters', this.filtersAsQueryParams)
        }
      }
    }
  }
</script>

<template>
  <form class="task-record-review-filters" @submit.prevent>
    <div class="row">
      <label class="col-3">
        {{ filters.predictedValues.name }}
        <multiselect class="mt-3 mb-5"
                     placeholder="Type here..."
                     v-model="selected.predictedValues"
                     :label="filters.predictedValues.label"
                     track-by="id"
                     multiple
                     hide-selected
                     taggable
                     tag-placeholder="Search for this exact value"
                     @tag="addArbitraryPredictedValue"
                     :options="filters.predictedValues.options" />
      </label>
      <label class="col-3">
        {{ filters.assignedTo.name }}
        <multiselect class="mt-3 mb-5"
                     placeholder="Type here..."
                     v-model="selected.assignedTo"
                     :label="filters.assignedTo.label"
                     track-by="id"
                     multiple
                     hide-selected
                     :options="filters.assignedTo.options" />
      </label>
      <label class="col-3">
        {{ filters.reviewedBy.name }}
        <multiselect class="mt-3 mb-5"
                     placeholder="Type here..."
                     v-model="selected.reviewedBy"
                     :label="filters.reviewedBy.label"
                     track-by="id"
                     multiple
                     hide-selected
                     :options="filters.reviewedBy.options" />
      </label>
      <label class="col-3">
        {{ filters.choices.name }}
        <multiselect class="mt-3 mb-5"
                     placeholder="Type here..."
                     v-model="selected.choices"
                     :label="filters.choices.label"
                     track-by="id"
                     multiple
                     hide-selected
                     :options="filters.choices.options" />
      </label>
    </div>
  </form>
</template>
