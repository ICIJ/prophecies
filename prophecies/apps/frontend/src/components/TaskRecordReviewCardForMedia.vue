<script>
import { get } from 'lodash'

import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import HapticCopyButton from '@/components/HapticCopyButton'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCardForMedia',
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
    HapticCopyButton,
    TaskRecordReviewCard
  },
  computed: {
    taskRecordReview() {
      return TaskRecordReview.query()
        .with('taskRecord')
        .with('taskRecord.medias')
        .find(this.taskRecordReviewId)
    },
    medias() {
      return get(this, 'taskRecordReview.taskRecord.medias', [])
    }
  },
  methods: {
    modalMediaId({ id }) {
      return `modal-task-record-media-${id}`
    }
  }
}
</script>

<template>
  <task-record-review-card
    class="task-record-review-card-for-media"
    v-on="$listeners"
    :task-record-review-id="taskRecordReviewId"
    :active="active"
    :selected="selected"
    :preview-link="previewLink"
    :frozen="frozen"
    :highlight-note="highlightNote">
    <template #original-value="{ taskRecord }">
      <div v-for="media in medias" :key="media.id">
        <div class="task-record-review-card-for-media__media mb-1">
          <div class="task-record-review-card-for-media__media__original-value">
            <haptic-copy-button :text="taskRecord.originalValue" class="btn-sm py-1 px-2 mx-auto" />
          </div>
          <template v-if="media.mediaType === 'IMAGE'">
            <a :href="media.file" target="_blank" v-b-modal="modalMediaId(media)" @click.prevent>
              <img
              :alt="taskRecord.originalValue"
              :src="media.file"
              class="img-fluid" />
            </a>
            <b-modal
               :id="modalMediaId(media)"
               content-class="bg-transparent text-center border-0 shadow-none pointer-events-none"
               header-class="border-0 p-0"
               dialog-class="mw-100 mx-4 px-3"
               hide-footer
               body-class="px-0"
               lazy
               size="xl">
              <template #modal-header="{ close }">
                <div class="d-flex w-100">
                  <b-btn class="pointer-events-all px-2 ml-auto text-light" variant="link" @click="close">
                    <x-icon />
                    <span class="sr-only">{{ $t('app.close') }}</span>
                  </b-btn>
                </div>
              </template>
              <div class="pointer-events-all mx-auto d-inline-block">
                <img
                  :alt="taskRecord.originalValue"
                  :src="media.file"
                  class="img-fluid mb-1 border shadow-lg" />
                <haptic-copy-button :text="taskRecord.originalValue" class="btn-sm py-1 px-2 mx-auto" />
              </div>
            </b-modal>
          </template>
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
