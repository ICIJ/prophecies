<script>
import { get } from 'lodash'

import TaskRecordReview from '@/models/TaskRecordReview'
import TaskRecordReviewCardForMedia from '@/components/TaskRecordReviewCardForMedia'
import TaskRecordReviewCardForIframe from '@/components/TaskRecordReviewCardForIframe'
import TaskRecordReviewCardForText from '@/components/TaskRecordReviewCardForText'

export default {
  name: 'TaskRecordReviewCardWrapper',
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
  computed: {
    is() {
      switch (this.taskTemplateType.toUpperCase()) {
        case 'MEDIA':
          return TaskRecordReviewCardForMedia
        case 'IFRAME':
          return TaskRecordReviewCardForIframe
        default:
          return TaskRecordReviewCardForText
      }
    },
    taskRecordReview() {
      return TaskRecordReview.query().with('taskRecord').with('taskRecord.task').find(this.taskRecordReviewId)
    },
    task() {
      return get(this, 'taskRecordReview.taskRecord.task')
    },
    taskTemplateType() {
      return get(this, 'task.templateType', '').toUpperCase()
    }
  }
}
</script>

<template>
  <component
    :is="is"
    :task-record-review-id="taskRecordReviewId"
    :active="active"
    :selected="selected"
    :preview-link="previewLink"
    :frozen="frozen"
    :highlight-note="highlightNote"
    v-on="$listeners"
  />
</template>
