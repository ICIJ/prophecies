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
    classList() {
      return {
        'task-record-review-actions--done': this.isDone,
        'task-record-review-actions--pending': this.isPending
      }
    },
    isDone() {
      return get(this, 'taskRecordReview.status') === 'DONE'
    },
    isPending() {
      return get(this, 'taskRecordReview.status') === 'PENDING'
    },
    taskRecordReview() {
      return TaskRecordReview.query()
        .with('task')
        .with('taskRecord')
        .with('taskRecord.lockedBy')
        .find(this.taskRecordReviewId)
    },
    taskIsOpen() {
      return this.taskStatus === TaskStatusEnum.OPEN
    },
    taskStatus() {
      return this.taskRecordReview.task.status
    },
    taskRecord() {
      return get(this, 'taskRecordReview.taskRecord')
    },
    taskRecordRoute() {
      return {
        name: 'task-record-review-retrieve',
        params: {
          taskId: this.taskRecordReview.taskId,
          taskRecordReviewId: this.taskRecordReviewId
        }
      }
    },
    unlock() {
      return this.$t('taskRecordReviewActions.unlock')
    }
  },
  methods: {
    emitCopy() {
      /**
       * @event copy
       * @param TaskRecordReview
       */
      this.$emit('copy', this.taskRecordReview)
    },
    emitLock() {
      /**
       * @event lock
       * @param TaskRecordReview
       */
      this.$emit('lock', this.taskRecordReview)
    },
    emitUnlock() {
      /**
       * @event unlock
       * @param TaskRecordReview
       */
      this.$emit('unlock', this.taskRecordReview)
    },
    emitBookmark() {
      /**
       * @event bookmark
       * @param TaskRecordReview
       */
      this.$emit('bookmark', this.taskRecordReview)
    },
    emitUnbookmark() {
      /**
       * @event unbookmark
       * @param TaskRecordReview
       */
      this.$emit('unbookmark', this.taskRecordReview)
    },
    emitToggleChanges() {
      /**
       * @event emitToggleChanges
       * @param TaskRecordReview
       */
      this.$emit('toggle-changes', this.taskRecordReview)
    },
    lockedBy(username) {
      return this.$t('taskRecordReviewActions.lockedBy', { username })
    }
  }
}
</script>

<template>
  <div class="task-record-review-actions" :class="classList">
    <b-btn-group vertical size="sm">
      <b-btn
        v-b-tooltip.left
        variant="link"
        class="text-dark"
        :to="taskRecordRoute"
        :title="$t('taskRecordReviewActions.openInANewWindow')"
        target="_blank"
      >
        <external-link-icon size="1.5x" />
        <span class="sr-only">{{ $t('taskRecordReviewActions.link') }}</span>
      </b-btn>
      <b-btn
        v-if="!taskRecord.bookmarked"
        v-b-tooltip.left
        variant="link"
        class="text-dark"
        :title="$t('taskRecordReviewActions.bookmark')"
        @click="emitBookmark"
      >
        <bookmark-icon size="1.5x" />
        <span class="sr-only">{{ $t('taskRecordReviewActions.bookmark') }}</span>
      </b-btn>
      <b-btn
        v-else
        v-b-tooltip.left
        variant="link"
        class="text-dark"
        :title="$t('taskRecordReviewActions.removeBookmark')"
        @click="emitUnbookmark"
      >
        <bookmark-icon size="1.5x" fill="currentColor" />
        <span class="sr-only">{{ $t('taskRecordReviewActions.removeBookmark') }}</span>
      </b-btn>
      <b-btn
        v-b-tooltip.left
        variant="link"
        disabled
        class="text-dark"
        :title="$t('taskRecordReviewActions.duplicateRecord')"
        @click="emitCopy"
      >
        <copy-icon size="1.5x" />
        <span class="sr-only">{{ $t('taskRecordReviewActions.duplicateRecord') }}</span>
      </b-btn>
      <b-btn
        v-if="!taskIsOpen"
        v-b-tooltip.left
        variant="link"
        class="text-danger task-record-review-actions__task_not_open"
        :title="$t('taskRecordReviewActions.adminMustOpenTheTask')"
      >
        <lock-icon size="1.5x" />
        <span class="sr-only">{{ unlock }}</span>
      </b-btn>
      <template v-else>
        <b-btn
          v-if="taskRecord.lockedByMe"
          v-b-tooltip.left
          variant="link"
          class="text-dark"
          :title="$t('taskRecordReviewActions.unlockRecord')"
          @click="emitUnlock"
        >
          <lock-icon size="1.5x" />
          <span class="sr-only">{{ unlock }}</span>
        </b-btn>
        <b-btn
          v-if="taskRecord.lockedByOther"
          v-b-tooltip.left
          variant="link"
          class="text-danger"
          :title="lockedBy(taskRecord.lockedBy.displayName)"
        >
          <lock-icon size="1.5x" />
          <span class="sr-only">{{ unlock }}</span>
        </b-btn>
        <b-btn
          v-if="!taskRecord.locked"
          v-b-tooltip.left
          variant="link"
          class="text-dark"
          :title="$t('taskRecordReviewActions.lockRecord')"
          @click="emitLock"
        >
          <unlock-icon size="1.5x" />
          <span class="sr-only">{{ $t('taskRecordReviewActions.lock') }}</span>
        </b-btn>
      </template>
      <b-btn
        v-b-tooltip.left
        variant="link"
        class="text-dark"
        :title="$t('taskRecordReviewActions.seeHistory')"
        @click="emitToggleChanges"
      >
        <clock-icon size="1.5x" />
        <span class="sr-only">{{ $t('taskRecordReviewActions.seeHistoryChanges') }}</span>
      </b-btn>
    </b-btn-group>
  </div>
</template>
