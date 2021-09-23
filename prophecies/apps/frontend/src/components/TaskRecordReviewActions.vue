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
        .with('task')
        .with('taskRecord')
        .with('taskRecord.lockedBy')
        .find(this.taskRecordReviewId)
    },
    taskIsOpen () {
      return this.taskStatus === 'OPEN' 
    },
    taskStatus(){
      return this.taskRecordReview.task.status
    },
    taskRecord () {
      return get(this, 'taskRecordReview.taskRecord')
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
    emitLock () {
      /**
       * @event lock
       * @param TaskRecordReview
       */
      this.$emit('lock', this.taskRecordReview)
    },
    emitUnlock () {
      /**
       * @event unlock
       * @param TaskRecordReview
       */
      this.$emit('unlock', this.taskRecordReview)
    },
    emitToggleChanges () {
      /**
       * @event emitToggleChanges
       * @param TaskRecordReview
       */
      this.$emit('toggle-changes', this.taskRecordReview)
    }
  }
}
</script>

<template>
  <div class="task-record-review-actions" :class="classList">
    <b-btn-group vertical size="sm">
      <b-btn variant="link" class="text-dark" :href="link"  v-if="link" title="Link" v-b-tooltip.left>
        <link-icon size="1.5x" />
        <span class="sr-only">Link</span>
      </b-btn>
      <b-btn variant="link" class="text-dark" title="Duplicate record" v-b-tooltip.left @click="emitCopy">
        <copy-icon size="1.5x" />
        <span class="sr-only">Duplicate record</span>
      </b-btn>
      <b-btn variant="link" v-if="!taskIsOpen" class="text-danger task-record-review-actions__task_not_open" :title="`The admin must open the task to let you review this record`" v-b-tooltip.left>
        <lock-icon size="1.5x" />
        <span class="sr-only">Unlock</span>
      </b-btn>
      <template v-else>
        <b-btn variant="link" v-if="taskRecord.lockedByMe" class="text-dark" title="Unlock record" v-b-tooltip.left @click="emitUnlock">
          <lock-icon size="1.5x" />
          <span class="sr-only">Unlock</span>
        </b-btn>
        <b-btn variant="link" v-if="taskRecord.lockedByOther" class="text-danger" :title="`${taskRecord.lockedBy.displayName} must unlock this record to let you review it`" v-b-tooltip.left>
          <lock-icon size="1.5x" />
          <span class="sr-only">Unlock</span>
        </b-btn>
        <b-btn variant="link" v-if="!taskRecord.locked" class="text-dark" title="Lock record (nobody will be able to review it until you unlock it)" v-b-tooltip.left @click="emitLock">
          <unlock-icon size="1.5x" />
          <span class="sr-only">Lock</span>
        </b-btn>
      </template>
      <b-btn variant="link" class="text-dark" title="See history" v-b-tooltip.left @click="emitToggleChanges">
        <clock-icon size="1.5x" />
        <span class="sr-only">See changes history</span>
      </b-btn>
    </b-btn-group>
  </div>
</template>
