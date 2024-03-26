<script>
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'

export default {
  name: 'TaskRecordReviewCardForText',
  components: {
    TaskRecordReviewCard
  },
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
  }
}
</script>

<template>
  <task-record-review-card
    :task-record-review-id="taskRecordReviewId"
    :active="active"
    :selected="selected"
    :preview-link="previewLink"
    :frozen="frozen"
    :highlight-note="highlightNote"
    v-on="$listeners"
  />
</template>
