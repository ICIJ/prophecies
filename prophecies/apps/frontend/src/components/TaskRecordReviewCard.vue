<script>
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCard',
  components: {
    TaskRecordReviewChoiceForm
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
    classList () {
      return {
        'shadow-lg': this.active,
        'shadow-sm': !this.active
      }
    }
  }
}
</script>

<template>
  <div class="task-record-review-card card card-body py-5 px-4" :class="classList">
    <div class="row align-items-center">
      <div class="task-record-review-card__id col-auto font-weight-bold">
        {{ taskRecordReview.id }}
      </div>
      <div class="task-record-review-card__original-value col-3 font-weight-bold">
        {{ taskRecordReview.task_record.original_value }}
      </div>
      <div class="task-record-review-card__original-value col-1 font-weight-bold">
        {{ taskRecordReview.task_record.predicted_value }}
      </div>
      <div class="task-record-review-card__choice col-5">
        <div class="row align-items-center">
          <div class="task-record-review-card__choice__form col-lg">
            <task-record-review-choice-form :task-record-review-id="taskRecordReviewId" />
          </div>
          <div class="task-record-review-card__choice_history col-lg">
            <b-badge variant="light">History</b-badge>
          </div>
        </div>
      </div>
      <div class="task-record-review-card__actions col-auto">
        <b-badge variant="light">Actions</b-badge>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scope>
  .task-record-review-card {
    &:hover {
      box-shadow: $box-shadow-lg !important;
    }
  }
</style>
