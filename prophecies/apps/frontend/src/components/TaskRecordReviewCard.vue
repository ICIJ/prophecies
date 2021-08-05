<script>
import { get } from 'lodash'
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
    }
  }
}
</script>

<template>
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
          <div class="task-record-review-card__choice__form col-lg">
            <task-record-review-choice-form :task-record-review-id="taskRecordReviewId" />
          </div>
          <div class="task-record-review-card__choice_history col-lg">
            <task-record-review-history :task-record-review-id="taskRecordReviewId" />
          </div>
        </div>
      </div>
      <div class="task-record-review-card__actions col-auto">
        <b-badge variant="light">Actions</b-badge>
      </div>
    </div>
  </div>
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
