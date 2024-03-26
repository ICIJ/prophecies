<script>
import { get, uniqueId } from 'lodash'

import TaskRecord from '@/models/TaskRecord'
import HapticCopyButton from '@/components/HapticCopyButton'

export default {
  name: 'TaskRecordIframe',
  components: {
    HapticCopyButton
  },
  props: {
    taskRecordId: {
      type: [String, Number]
    },
    expand: {
      type: Boolean
    },
    hidden: {
      type: Boolean
    },
    lazy: {
      type: Boolean
    }
  },
  data() {
    return {
      observer: null,
      isIntersecting: false
    }
  },
  computed: {
    taskRecord() {
      return TaskRecord.query().with('task').with('task.templateSetting').find(this.taskRecordId)
    },
    templateSetting() {
      return get(this, 'taskRecord.task.templateSetting', {})
    },
    embeddableLink() {
      return get(this, 'taskRecord.embeddableLink')
    },
    embeddableLinkIfVisible() {
      if (this.visible) {
        return this.embeddableLink
      }
      return 'about:blank'
    },
    modalId() {
      return uniqueId(`modal-task-record-iframe-${this.taskRecordId}-`)
    },
    style() {
      return {
        '--iframe-ratio': get(this, 'templateSetting.ratio', 1)
      }
    },
    displayOriginalValue() {
      return this.templateSetting?.displayOriginalValue
    },
    visible() {
      return !this.hidden && (!this.lazy || this.isIntersecting)
    }
  },
  mounted() {
    if (this.lazy) {
      this.bindObserver()
    }
  },
  methods: {
    bindObserver() {
      this.observer = new IntersectionObserver((entries) => {
        this.isIntersecting = this.isIntersecting || entries[0].isIntersecting
      })
      this.observer.observe(this.$el)
    }
  }
}
</script>

<template>
  <div class="task-record-iframe" :style="style">
    <iframe
      :src="embeddableLinkIfVisible"
      class="border"
      style="border: 0"
      loading="lazy"
      allowfullscreen
      width="100%"
      height="100%"
    />
    <button v-if="expand" v-b-modal="modalId" class="task-record-iframe__expand btn btn-link p-1 m-1">
      <maximize-2-icon />
    </button>
    <b-modal
      v-if="expand"
      :id="modalId"
      content-class="bg-transparent text-center border-0 shadow-none pointer-events-none"
      header-class="border-0 p-0"
      dialog-class="mx-auto px-3"
      hide-footer
      body-class="px-0"
      lazy
      size="lg"
    >
      <template #modal-header="{ close }">
        <div class="d-flex w-100">
          <b-btn class="pointer-events-all px-2 ml-auto text-light" variant="link" @click="close">
            <x-icon />
            <span class="sr-only">{{ $t('app.close') }}</span>
          </b-btn>
        </div>
      </template>
      <div class="pointer-events-all mx-auto d-inline-block w-100">
        <task-record-iframe :task-record-id="taskRecordId" class="mb-3" />
        <haptic-copy-button
          v-if="displayOriginalValue"
          :text="taskRecord.originalValue"
          class="btn-sm py-1 px-2 mx-auto"
        />
      </div>
    </b-modal>
  </div>
</template>

<style lang="scss" scoped>
.task-record-iframe {
  position: relative;
  display: block;
  padding-top: calc(100% * var(--iframe-ratio, 1));

  &__expand {
    position: absolute;
    right: 0;
    top: 0;
    z-index: 10;
    background: rgba(#fff, 0.5);

    &:hover {
      background-color: #fff;
    }
  }

  & > iframe {
    z-index: 0;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0;
  }
}
</style>
