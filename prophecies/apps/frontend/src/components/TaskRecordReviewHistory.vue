<script>
import { toVariant } from '@/utils/variant'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewHistory',
  filters: {
    toVariant
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    }
  },
  computed: {
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('checker')
        .with('choice')
        .with('history')
        .with('history.checker')
        .with('history.choice')
        .find(this.taskRecordReviewId)
    },
    taskRecordId () {
      return this.taskRecordReview.task_record_id
    },
    history () {
      return [this.taskRecordReview, ...this.taskRecordReview.history]
    },
    classList () {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue,
        'task-record-review-choice-form--has-note': this.hasNote
      }
    }
  }
}
</script>

<template>
  <div class="task-record-review-history">
    <div class="d-flex" v-for="{ id, checker, choice, note } in history" :key="id">
      <div class="py-1">
        {{ checker.first_name || checker.username }}:
      </div>
      <div class="">
        <b-badge :variant="choice.value | toVariant" v-if="choice">
          {{ choice.name[0] }}
        </b-badge>
      </div>
    </div>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-history {
  }
</style>
