<script>
import moment from 'moment'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewNoteTimestamp',
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    }
  },
  computed: {
    taskRecordReview () {
      return TaskRecordReview.find(this.taskRecordReviewId)
    },
    route () {
      return {
        name: 'task-record-review-retrieve',
        params: {
          taskId: this.taskRecordReview.taskId,
          taskRecordReviewId: this.taskRecordReviewId
        },
        query: {
          highlightNote: true
        }
      }
    },
    noteCreatedAtTitle () {
      const noteCreatedAt = this.taskRecordReview.noteCreatedAt
      return this.$options.filters.formatDateLong(noteCreatedAt)
    },
    noteUpdatedAtTitle () {
      const noteUpdatedAt = this.taskRecordReview.noteUpdatedAt
      return this.$options.filters.formatDateLong(noteUpdatedAt)
    }
  },
  filters: {
    formatDateLong (d) {
      return moment(d).format('MMM Do YYYY - hh:mm')
    },
    formatDateFromNow (d) {
      return moment(d).fromNow()
    }
  }
}
</script>

<template>
  <span class="task-record-review-note-timestamp">
    <template v-if="taskRecordReview.noteUpdatedAt">
      <router-link :to="this.route" :title="noteUpdatedAtTitle" v-b-tooltip.hover class="task-record-review-note-timestamp__link">
        {{ taskRecordReview.noteUpdatedAt | formatDateFromNow }} (edited)
      </router-link>
    </template>
    <template v-else-if="taskRecordReview.noteCreatedAt">
      <router-link :to="this.route" :title="noteCreatedAtTitle" v-b-tooltip.hover class="task-record-review-note-timestamp__link">
        {{ taskRecordReview.noteCreatedAt | formatDateFromNow }}
      </router-link>
    </template>
  </span>
</template>

<style scoped>
  .task-record-review-note-timestamp__link {
    color: inherit;
  }
</style>
