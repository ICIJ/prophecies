<script>
import { uniqueId } from 'lodash'
import TaskRecordMedia from '@/models/TaskRecordMedia'

import HapticCopyButton from '@/components/HapticCopyButton'

export default {
  name: 'TaskRecordMediaView',
  props: {
    taskRecordMediaId: {
      type: [String, Number]
    },
    expand: {
      type: Boolean
    }
  },
  components: {
    HapticCopyButton
  },
  computed: {
    taskRecordMedia() {
      return TaskRecordMedia.query()
        .with('taskRecord')
        .find(this.taskRecordMediaId)
    },
    taskRecord() {
      return this.taskRecordMedia.taskRecord
    },
    file() {
      return this.taskRecordMedia.file
    },
    isImage() {
      return this.taskRecordMedia?.mediaType?.toUpperCase() === 'IMAGE'
    },
    modalId() {
      return uniqueId(`modal-task-record-media-${this.taskRecordMediaId}-`)
    }
  },
  methods: {
    mightPrevent(event) {
      if (this.expand) {
        event.preventDefault()
      }
    }
  }
}
</script>

<template>
  <div class="task-record-media">
    <template v-if="isImage">
      <a
        :href="file"
        class="task-record-media__link"
        target="_blank"
        v-b-modal="modalId"
        @click="mightPrevent">
        <img
          :alt="taskRecord.originalValue"
          :src="file"
          class="task-record-media__link__view img-fluid" />
        <span v-if="expand" class="task-record-media__link__expand">
          <maximize-2-icon />
        </span>
      </a>
    </template>
    <b-modal
        v-if="expand"
        :id="modalId"
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
        <task-record-media-view :task-record-media-id="taskRecordMediaId" class="mb-1" />
        <haptic-copy-button :text="taskRecord.originalValue" class="btn-sm py-1 px-2 mx-auto" />
      </div>
    </b-modal>
  </div>
</template>

<style lang="scss" scoped>
.task-record-media {
  &__link {
    z-index: 0;
    position: relative;
    display: inline-block;

    &:hover &__expand {
      opacity: 1;
    }

    &__expand {
      position: absolute;
      top: 0;
      right: 0;
      padding: $spacer;
      opacity: 0.5;
    }
  }
}
</style>
