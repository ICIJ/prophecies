<script>
import { get } from 'lodash'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewActions',
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    }
  },
  computed: {
    classList () {
      return {
        'task-record-review-actions--done': this.isDone,
        'task-record-review-actions--pending': this.isPending
      }
    },
    isDone () {
      return get(this, 'taskRecordReview.status') === 'DONE'
    },
    isPending () {
      return get(this, 'taskRecordReview.status') === 'PENDING'
    },
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('task_record')
        .find(this.taskRecordReviewId)
    },
    link () {
      return get(this, 'taskRecordReview.task_record.link')
    }
  }
}
</script>

<template>
  <div class="task-record-review-actions" :class="classList">
    <b-button-group vertical size="sm">
      <b-button variant="link" class="text-dark" :href="link" target="_blank" v-if="link" title="Link" v-b-tooltip.left>
        <link-icon size="1.5x" />
        <span class="sr-only">Link</span>
      </b-button>
      <b-button variant="link" class="text-dark" title="Copy" v-b-tooltip.left>
        <copy-icon size="1.5x" />
        <span class="sr-only">Copy</span>
      </b-button>
      <b-button variant="link" class="text-dark" title="Lock" v-b-tooltip.left>
        <unlock-icon size="1.5x" />
        <span class="sr-only">Lock</span>
      </b-button>
      <b-button variant="link" class="text-dark" title="See history" v-b-tooltip.left>
        <clock-icon size="1.5x" />
        <span class="sr-only">See history</span>
      </b-button>
    </b-button-group>
  </div>
</template>
