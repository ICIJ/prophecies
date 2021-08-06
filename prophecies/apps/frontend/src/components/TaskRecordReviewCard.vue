<script>
import { get, uniqueId } from 'lodash'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'
import TaskRecordReviewHistory from '@/components/TaskRecordReviewHistory'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCard',
  components: {
    TaskRecordReviewChoiceForm,
    TaskRecordReviewHistory
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
      /**
       * @event Fired when the task record review is updated
       */
      this.$emit('update', data)
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
    <div class="task-record-review-card card card-body py-5 px-4" :class="classList">
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
        <div class="task-record-review-card__choice col-6">
          <div class="row align-items-center">
            <div class="task-record-review-card__choice__form col-lg-6">
              <task-record-review-choice-form @submit="selectChoiceWithLoader" :task-record-review-id="taskRecordReviewId" />
            </div>
            <div class="task-record-review-card__choice_history col-lg-6">
              <task-record-review-history :task-record-review-id="taskRecordReviewId" />
            </div>
          </div>
        </div>
        <div class="task-record-review-card__actions col-auto">
          <b-badge variant="light">
            Actions
          </b-badge>
        </div>
      </div>
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
  }
</style>
