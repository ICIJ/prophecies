<script>
import { keys } from 'lodash'
import Multiselect from 'vue-multiselect'

import MultiselectButtons from '@/components/MultiselectButtons'
import taskRecordReviewFiltersMixin from '@/mixins/task-record-review-filters'
import Task from '@/models/Task'

export default {
  name: 'TaskRecordReviewFilters',
  components: {
    Multiselect,
    MultiselectButtons
  },
  mixins: [taskRecordReviewFiltersMixin],
  props: {
    taskId: {
      type: [Number, String]
    },
    routeFilters: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
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
        hasNotes: [],
        bookmarkedBy: [],
        hasAllRoundsReviewed: []
      }
    }
  },
  computed: {
    filters() {
      // Method from the mixins
      return this.getTaskFilters(this.task)
    },
    task() {
      return Task.query()
        .with('checkers')
        .with('choiceGroup')
        .with('choiceGroup.alternativeValues')
        .with('choiceGroup.choices')
        .find(this.taskId)
    },
    filtersAsQueryParams() {
      // Method from the mixins
      return this.getSelectedFiltersAsRouteFilters(this.filters, this.selected)
    }
  },
  watch: {
    routeFilters: {
      deep: true,
      handler() {
        this.readRouteFilters()
      }
    },
    selected: {
      deep: true,
      handler(u) {
        /**
         * @event update:routeFilters
         * @param routes query params after updating filters
         */
        this.$emit('update:routeFilters', this.filtersAsQueryParams)
      }
    }
  },
  created() {
    this.readRouteFilters()
  },
  methods: {
    addArbitraryPredictedValue(value) {
      // Method from the mixins
      const option = this.toSerializableOption(value)
      this.selected.predictedValues.push(option)
    },
    addAlternativeValues(value) {
      // Method from the mixins
      const option = this.toSerializableOption(value)
      this.selected.alternativeValues.push(option)
    },
    readRouteFilters() {
      // Clear all keys
      keys(this.selected).forEach((key) => this.$set(this.selected, key, []))
      // Method from the mixins
      const options = this.mapRouteQueryToFilterOptions(this.routeFilters, this.task)
      // Apply the selected options to each filter
      options.forEach(([key, option]) => this.$set(this.selected, key, option))
    }
  }
}
</script>

<template>
  <form class="task-record-review-filters mb-3" @submit.prevent>
    <div class="row">
      <label class="col-12 col-sm-6 col-lg">
        {{ filters.predictedValues.name }}
        <multiselect
          v-model="selected.predictedValues"
          class="mt-3 mb-3"
          placeholder="Type here..."
          :label="filters.predictedValues.label"
          track-by="id"
          multiple
          taggable
          tag-placeholder="Search for this exact value"
          tag-position="bottom"
          :options="filters.predictedValues.options"
          @tag="addArbitraryPredictedValue"
        />
      </label>
      <label class="col-12 col-sm-6 col-lg">
        {{ filters.assignedTo.name }}
        <multiselect
          v-model="selected.assignedTo"
          class="mt-3 mb-3"
          placeholder="Type here..."
          :label="filters.assignedTo.label"
          track-by="id"
          multiple
          :options="filters.assignedTo.options"
        />
      </label>
      <label class="col-12 col-sm-6 col-lg">
        {{ filters.bookmarkedBy.name }}
        <multiselect
          v-model="selected.bookmarkedBy"
          class="mt-3 mb-3"
          placeholder="Type here..."
          :label="filters.bookmarkedBy.label"
          track-by="id"
          multiple
          :options="filters.bookmarkedBy.options"
        />
      </label>

      <label class="col-12 col-sm-6 col-lg">
        {{ filters.alternativeValues.name }}
        <multiselect
          v-model="selected.alternativeValues"
          class="mt-3 mb-3"
          placeholder="Type here..."
          :label="filters.alternativeValues.label"
          track-by="id"
          multiple
          taggable
          tag-placeholder="Search for this exact value"
          tag-position="bottom"
          :options="filters.alternativeValues.options"
          @tag="addAlternativeValues"
        />
      </label>
      <label class="col-12 col-sm-6 col-lg">
        {{ filters.choices.name }}
        <multiselect
          v-model="selected.choices"
          class="mt-3 mb-3"
          placeholder="Type here..."
          :label="filters.choices.label"
          track-by="id"
          multiple
          :options="filters.choices.options"
        />
      </label>
    </div>
    <div class="row">
      <div class="col-12 col-md-6 col-lg">
        {{ filters.priorities.name }}
        <multiselect-buttons
          v-model="selected.priorities"
          class="mt-3 mb-3 text-nowrap"
          multiple
          label="label"
          track-by="label"
          :options="filters.priorities.options"
        />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.rounds.name }}
        <multiselect-buttons
          v-model="selected.rounds"
          class="mt-3 mb-3 text-nowrap"
          multiple
          label="label"
          track-by="label"
          :options="filters.rounds.options"
        />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.hasDisagreements.name }}
        <multiselect-buttons
          v-model="selected.hasDisagreements"
          class="mt-3 mb-3 text-nowrap"
          label="label"
          track-by="label"
          :options="filters.hasDisagreements.options"
        />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.locked.name }}
        <multiselect-buttons
          v-model="selected.locked"
          class="mt-3 mb-3 text-nowrap"
          label="label"
          track-by="label"
          :options="filters.locked.options"
        />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.hasNotes.name }}
        <multiselect-buttons
          v-model="selected.hasNotes"
          class="mt-3 mb-3 text-nowrap"
          label="label"
          track-by="label"
          :options="filters.hasNotes.options"
        />
      </div>
      <div class="col-12 col-md-6 col-lg">
        {{ filters.hasAllRoundsReviewed.name }}
        <multiselect-buttons
          v-model="selected.hasAllRoundsReviewed"
          class="mt-3 mb-3 text-nowrap"
          placeholder="Type here..."
          label="label"
          track-by="name"
          :options="filters.hasAllRoundsReviewed.options"
        />
      </div>
    </div>
  </form>
</template>
