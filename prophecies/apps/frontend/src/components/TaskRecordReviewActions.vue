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
        .with('taskRecord')
        .find(this.taskRecordReviewId)
    },
    link () {
      return get(this, 'taskRecordReview.taskRecord.link')
    }
  },
  methods: {
    emitCopy () {
      /**
       * @event copy
       * @param TaskRecordReview
       */
      this.$emit('copy', this.taskRecordReview)
    },
    emitToggleLock () {
      /**
       * @event toggle-lock
       * @param TaskRecordReview
       */
      this.$emit('toggle-lock', this.taskRecordReview)
    },
    emitHistory () {
      /**
       * @event history
       * @param TaskRecordReview
       */
      this.$emit('history', this.taskRecordReview)
    }
  }
}
</script>

<template>
  <div class="task-record-review-actions" :class="classList">
    <b-btn-group vertical size="sm">
      <b-btn variant="link" class="text-dark" :href="link" target="_blank" v-if="link" title="Link" v-b-tooltip.left>
        <link-icon size="1.5x" />
        <span class="sr-only">Link</span>
      </b-btn>
      <b-btn variant="link" class="text-dark" title="Copy" v-b-tooltip.left @click="emitCopy">
        <copy-icon size="1.5x" />
        <span class="sr-only">Copy</span>
      </b-btn>
      <b-btn variant="link" class="text-dark" title="Lock" v-b-tooltip.left @click="emitToggleLock">
        <unlock-icon size="1.5x" />
        <span class="sr-only">Lock</span>
      </b-btn>
      <b-btn variant="link" class="text-dark" title="See history" v-b-tooltip.left @click="emitHistory">
        <clock-icon size="1.5x" />
        <span class="sr-only">See history</span>
      </b-btn>
    </b-btn-group>
  </div>
</template>
