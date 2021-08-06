<script>
import { get, uniqueId } from 'lodash'
import TaskRecordReviewActions from '@/components/TaskRecordReviewActions'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'
import TaskRecordReviewHistory from '@/components/TaskRecordReviewHistory'
import TaskRecordReviewNotes from '@/components/TaskRecordReviewNotes'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCard',
  components: {
    TaskRecordReviewActions,
    TaskRecordReviewChoiceForm,
    TaskRecordReviewHistory,
    TaskRecordReviewNotes
  },
  data () {
    return {
      showNotes: false
    }
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    active: {
      type: Boolean
    }
  },
  methods: {
    async selectChoiceWithLoader (data) {
      this.$wait.start(this.updateLoader)
      await this.selectChoice(data)
      this.$wait.end(this.updateLoader)
    },
    async selectChoice (data) {
      // We use a dedicated method that will format the data for the JSONAPI spec
      // and return the updated object (the store shall be updated as well).
      await TaskRecordReview.api().selectChoice(this.taskRecordReviewId, data)
      // Hide node to avoid using unecessary space
      this.showNotes = false
      /**
       * Fired when the task record review is updated
       * @event update
       * @param The updated attributes and relationships
       */
      this.$emit('update', data)
    },
    toggleNotes () {
      this.showNotes = !this.showNotes
    }
  },
  computed: {
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('task_record')
        .find(this.taskRecordReviewId)
    },
    isDone () {
      return get(this, 'taskRecordReview.status') === 'DONE'
    },
    isPending () {
      return get(this, 'taskRecordReview.status') === 'PENDING'
    },
    classList () {
      return {
        'task-record-review-card--active': this.active,
        'task-record-review-card--done': this.isDone,
        'task-record-review-card--pending': this.isPending
      }
    },
    updateLoader () {
      return uniqueId('update-task-record-review-')
    },
    overlayVariant () {
      if (this.taskRecordReview.status === 'DONE') {
        return 'lighter'
      }
      return 'white'
    }
  }
}
</script>

<template>
  <b-overlay :show="$wait.is(updateLoader)" :variant="overlayVariant" rounded="lg">
    <b-spinner variant="light" slot="overlay" />
    <div class="task-record-review-card card card-body p-4" :class="classList">
      <div class="row align-items-center">
        <div class="task-record-review-card__id col-auto font-weight-bold">
          {{ taskRecordReview.task_record.id }}
        </div>
        <div class="task-record-review-card__original-value col-3 font-weight-bold">
          {{ taskRecordReview.task_record.original_value }}
        </div>
        <div class="task-record-review-card__original-value col-1 font-weight-bold">
          {{ taskRecordReview.task_record.predicted_value }}
        </div>
        <div class="task-record-review-card__choice col">
          <div class="row align-items-center">
            <div class="task-record-review-card__choice__form col-xl-6">
              <task-record-review-choice-form @submit="selectChoiceWithLoader" :task-record-review-id="taskRecordReviewId" />
            </div>
            <div class="task-record-review-card__choice_history col-xl-6">
              <task-record-review-history :task-record-review-id="taskRecordReviewId" @toggle-notes="toggleNotes" />
            </div>
          </div>
        </div>
        <div class="task-record-review-card__actions col-auto">
          <task-record-review-actions :task-record-review-id="taskRecordReviewId" />
        </div>
      </div>
      <b-collapse :visible="showNotes">
        <task-record-review-notes :task-record-review-id="taskRecordReviewId" />
      </b-collapse>
    </div>
  </b-overlay>
</template>

<style lang="scss" scoped>
  .task-record-review-card {
    box-shadow: $box-shadow-sm;

    &--active {
      box-shadow: $box-shadow-lg;
      border: 1px solid $primary;
    }

    &--done {
      background: $lighter;
    }

    &__actions {
      min-width: 0;
      opacity: 0.25;
    }

    &:hover &__actions,
    &--active &__actions {
      opacity: 1;
    }
  }
</style>
