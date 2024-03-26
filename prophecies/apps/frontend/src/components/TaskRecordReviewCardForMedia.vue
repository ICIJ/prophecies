<script>
import { get } from 'lodash'

import TaskRecordMediaView from '@/components/TaskRecordMediaView'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import HapticCopyButton from '@/components/HapticCopyButton'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCardForMedia',
  components: {
    HapticCopyButton,
    TaskRecordMediaView,
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
        .with('taskRecord.medias')
        .find(this.taskRecordReviewId)
    },
    medias() {
      return get(this, 'taskRecordReview.taskRecord.medias', [])
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
    class="task-record-review-card-for-media"
    :task-record-review-id="taskRecordReviewId"
    :active="active"
    :selected="selected"
    :preview-link="previewLink"
    :frozen="frozen"
    :highlight-note="highlightNote"
    v-on="$listeners"
  >
    <template #original-value="{ taskRecord }">
      <div v-for="{ id } in medias" :key="id">
        <div class="task-record-review-card-for-media__media mb-1">
          <task-record-media-view :task-record-media-id="id" expand />
          <div v-if="displayOriginalValue" class="task-record-review-card-for-media__media__original-value">
            <haptic-copy-button :text="taskRecord.originalValue" class="btn-sm py-1 px-2 mx-auto" />
          </div>
        </div>
      </div>
    </template>
  </task-record-review-card>
</template>

<style lang="scss" scoped>
.task-record-review-card-for-media {
  &__media {
    min-height: 2rem;
    position: relative;
    border: 1px solid $border-color;
    background-color: #fff;

    &__original-value {
      text-align: center;
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: $spacer-xxs;
      font-weight: bold;
      opacity: 0.5;
      background: rgba(#fff, 0.5);
    }

    &:hover &__original-value {
      opacity: 1;
      background: rgba(#fff, 0.9);
    }
  }
}
</style>
