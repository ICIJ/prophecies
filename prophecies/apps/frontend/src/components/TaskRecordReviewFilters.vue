<script>
  import { find, keys, map, mapValues, trim, uniqueId } from 'lodash'
  import Multiselect from 'vue-multiselect'
  import MultiselectButtons from '@/components/MultiselectButtons'
  import taskRecordReviewFiltersMixin from '@/mixins/task-record-review-filters'
  import ChoiceGroup from '@/models/ChoiceGroup'
  import Task from '@/models/Task'
  import TaskRecordReview from '@/models/TaskRecordReview'

  export default {
    name: 'TaskRecordReviewFilters',
    mixins: [taskRecordReviewFiltersMixin],
    components: {
      Multiselect,
      MultiselectButtons
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
          alternativeValues: [],
          choices: [],
          priorities: [],
          rounds: [],
          hasDisagreements: [],
          locked: [],
          hasNotes: []
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
        return this.getSelectedFiltersAsRouteFilters(this.filters, this.selected)
      }
    },
    methods: {
      addArbitraryPredictedValue (value) {
        // Method from the mixins
        const option = this.toSerializableOption(value)
        this.selected.predictedValues.push(option)
      },
      addAlternativeValues (value) {
        // Method from the mixins
        const option = this.toSerializableOption(value)
        this.selected.alternativeValues.push(option)
      },
      readRouteFilters () {
        // Clear all keys
        keys(this.selected).forEach(key => this.$set(this.selected, key, []))
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
        handler (u) {
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
  <form class="task-record-review-filters mb-3" @submit.prevent>
    <div class="row">
      <label class="col-12 col-sm-6 col-lg-3">
        {{ filters.predictedValues.name }}
        <multiselect class="mt-3 mb-3"
                     placeholder="Type here..."
                     v-model="selected.predictedValues"
                     :label="filters.predictedValues.label"
                     track-by="id"
                     multiple
                     taggable
                     tag-placeholder="Search for this exact value"
                     tag-position="bottom"
                     @tag="addArbitraryPredictedValue"
                     :options="filters.predictedValues.options" />
      </label>
      <label class="col-12 col-sm-6 col-lg-3">
        {{ filters.assignedTo.name }}
        <multiselect class="mt-3 mb-3"
                     placeholder="Type here..."
                     v-model="selected.assignedTo"
                     :label="filters.assignedTo.label"
                     track-by="id"
                     multiple
                     :options="filters.assignedTo.options" />
      </label>
      <label class="col-12 col-sm-6 col-lg-3">
        {{ filters.alternativeValues.name }}
        <multiselect class="mt-3 mb-3"
                     placeholder="Type here..."
                     v-model="selected.alternativeValues"
                     :label="filters.alternativeValues.label"
                     track-by="id"
                     multiple
                     taggable
                     tag-placeholder="Search for this exact value"
                     tag-position="bottom"
                     @tag="addAlternativeValues"
                     :options="filters.alternativeValues.options" />
      </label>
      <label class="col-12 col-sm-6 col-lg-3">
        {{ filters.choices.name }}
        <multiselect class="mt-3 mb-3"
                     placeholder="Type here..."
                     v-model="selected.choices"
                     :label="filters.choices.label"
                     track-by="id"
                     multiple
                     :options="filters.choices.options" />
      </label>
    </div>
    <div class="row">
      <div class="col-12 col-md-6 col-lg">
        {{ filters.priorities.name }}
        <multiselect-buttons class="mt-3 mb-3 text-nowrap"
                     multiple
                     v-model="selected.priorities"
                     label="label"
                     track-by="label"
                     :options="filters.priorities.options" />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.rounds.name }}
        <multiselect-buttons class="mt-3 mb-3 text-nowrap"
                     multiple
                     v-model="selected.rounds"
                     label="label"
                     track-by="label"
                     :options="filters.rounds.options" />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.hasDisagreements.name }}
        <multiselect-buttons class="mt-3 mb-3 text-nowrap"
                     v-model="selected.hasDisagreements"
                     label="label"
                     track-by="label"
                     :options="filters.hasDisagreements.options" />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.locked.name }}
        <multiselect-buttons class="mt-3 mb-3 text-nowrap"
                    v-model="selected.locked"
                    label="label"
                    track-by="label"
                    :options="filters.locked.options" />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.hasNotes.name }}
        <multiselect-buttons class="mt-3 mb-3 text-nowrap"
                    v-model="selected.hasNotes"
                    label="label"
                    track-by="label"
                    :options="filters.hasNotes.options" />
      </div>
    </div>
  </form>
</template>
