<script>
import { get } from 'lodash'
import TaskRecordReview from '@/models/TaskRecordReview'
import { TaskStatusEnum } from '@/models/Task'

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
      return this.taskStatus === TaskStatusEnum.OPEN
    },
    taskStatus () {
      return this.taskRecordReview.task.status
    },
    taskRecord () {
      return get(this, 'taskRecordReview.taskRecord')
    },
    taskRecordRoute () {
      return {
        name: 'task-record-review-retrieve',
        params: {
          taskId: this.taskRecordReview.taskId,
          taskRecordReviewId: this.taskRecordReviewId
        }
      }
    },
    unlock () {
      return this.$t('taskRecordReviewActions.unlock')
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
    emitBookmark () {
      /**
       * @event bookmark
       * @param TaskRecordReview
       */
      this.$emit('bookmark', this.taskRecordReview)
    },
    emitUnbookmark () {
      /**
       * @event unbookmark
       * @param TaskRecordReview
       */
      this.$emit('unbookmark', this.taskRecordReview)
    },
    emitToggleChanges () {
      /**
       * @event emitToggleChanges
       * @param TaskRecordReview
       */
      this.$emit('toggle-changes', this.taskRecordReview)
    },
    lockedBy (username) {
      return this.$t('taskRecordReviewActions.lockedBy', { username })
    }
  }
}
</script>

<template>
  <div class="task-record-review-actions" :class="classList">
    <b-btn-group vertical size="sm">
      <b-btn variant="link" class="text-dark" :to="taskRecordRoute" :title="$t('taskRecordReviewActions.openInANewWindow')" v-b-tooltip.left target="_blank">
        <external-link-icon size="1.5x" />
        <span class="sr-only">{{$t('taskRecordReviewActions.link')}}</span>
      </b-btn>
       <b-btn variant="link" v-if="!taskRecord.bookmarked" class="text-dark" :title="$t('taskRecordReviewActions.bookmark')" v-b-tooltip.left @click="emitBookmark">
        <bookmark-icon size="1.5x"/>
        <span class="sr-only">{{$t('taskRecordReviewActions.bookmark')}}</span>
      </b-btn>
     <b-btn variant="link" v-else class="text-dark" :title="$t('taskRecordReviewActions.removeBookmark')" v-b-tooltip.left @click="emitUnbookmark">
        <bookmark-icon size="1.5x" fill="currentColor"/>
        <span class="sr-only">{{$t('taskRecordReviewActions.removeBookmark')}}</span>
      </b-btn>
     <b-btn variant="link" disabled class="text-dark" :title="$t('taskRecordReviewActions.duplicateRecord')" v-b-tooltip.left @click="emitCopy">
        <copy-icon size="1.5x" />
        <span class="sr-only">{{$t('taskRecordReviewActions.duplicateRecord')}}</span>
      </b-btn>
      <b-btn variant="link" v-if="!taskIsOpen" class="text-danger task-record-review-actions__task_not_open" :title="$t('taskRecordReviewActions.adminMustOpenTheTask')" v-b-tooltip.left>
        <lock-icon size="1.5x" />
        <span class="sr-only">{{unlock}}</span>
      </b-btn>
      <template v-else>
        <b-btn variant="link" v-if="taskRecord.lockedByMe" class="text-dark" :title="$t('taskRecordReviewActions.unlockRecord')" v-b-tooltip.left @click="emitUnlock">
          <lock-icon size="1.5x" />
          <span class="sr-only">{{unlock}}</span>
        </b-btn>
        <b-btn variant="link" v-if="taskRecord.lockedByOther" class="text-danger" :title="lockedBy(taskRecord.lockedBy.displayName)" v-b-tooltip.left>
          <lock-icon size="1.5x" />
          <span class="sr-only">{{unlock}}</span>
        </b-btn>
        <b-btn variant="link" v-if="!taskRecord.locked" class="text-dark" :title="$t('taskRecordReviewActions.lockRecord')" v-b-tooltip.left @click="emitLock">
          <unlock-icon size="1.5x" />
          <span class="sr-only">{{$t('taskRecordReviewActions.lock')}}</span>
        </b-btn>
      </template>
      <b-btn variant="link" class="text-dark" :title="$t('taskRecordReviewActions.seeHistory')" v-b-tooltip.left @click="emitToggleChanges">
        <clock-icon size="1.5x" />
        <span class="sr-only">{{$t('taskRecordReviewActions.seeHistoryChanges')}}</span>
      </b-btn>
    </b-btn-group>
  </div>
</template>
