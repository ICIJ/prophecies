<script>
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'

export default {
  name: 'TaskRecordReviewCardForText',
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    active: {
      type: Boolean
    },
    selected: {
      type: Boolean
    },
    previewLink: {
      type: Boolean
    },
    frozen: {
      type: Boolean
    },
    highlightNote: {
      type: [Boolean, String]
    }
  },
  components: {
    TaskRecordReviewCard
  }
}
</script>

<template>
  <task-record-review-card
    v-on="$listeners"
    :task-record-review-id="taskRecordReviewId"
    :active="active"
    :selected="selected"
    :preview-link="previewLink"
    :frozen="frozen"
    :highlight-note="highlightNote" />
</template>
