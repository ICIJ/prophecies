<script>
import { get } from 'lodash'

import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import TaskRecordIframe from '@/components/TaskRecordIframe'
import HapticCopyButton from '@/components/HapticCopyButton'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCardForIframe',
  components: {
    HapticCopyButton,
    TaskRecordIframe,
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
  },
  computed: {
    taskRecordReview() {
      return TaskRecordReview.query()
        .with('taskRecord')
        .with('taskRecord.task')
        .with('taskRecord.task.templateSetting')
        .find(this.taskRecordReviewId)
    },
    templateSetting() {
      return get(this, 'taskRecordReview.taskRecord.task.templateSetting', {})
    },
    displayOriginalValue() {
      return this.templateSetting?.displayOriginalValue
    }
  }
}
</script>

<template>
  <task-record-review-card
    class="task-record-review-card-for-iframe"
    no-link
    no-embed
    :task-record-review-id="taskRecordReviewId"
    :active="active"
    :selected="selected"
    :preview-link="previewLink"
    :frozen="frozen"
    :highlight-note="highlightNote"
    v-on="$listeners"
  >
    <template #original-value="{ taskRecord }">
      <task-record-iframe :task-record-id="taskRecordReview.taskRecordId" expand lazy class="mb-3" />
      <haptic-copy-button
        v-if="displayOriginalValue"
        :text="taskRecord.originalValue"
        class="btn-sm mx-auto py-1 px-2"
      />
    </template>
  </task-record-review-card>
</template>
