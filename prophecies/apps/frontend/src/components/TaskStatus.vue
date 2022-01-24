<script>
import { camelCase, kebabCase } from 'lodash'
import Task, { TaskStatusEnum } from '@/models/Task'

export default {
  name: 'TaskStatus',
  props: {
    taskId: {
      type: [String, Number]
    }
  },
  computed: {
    classList  () {
      return [`task-status--${kebabCase(this.status)}`]
    },
    icon () {
      switch (this.status) {
        case TaskStatusEnum.OPEN:
          return 'CheckIcon'
        case TaskStatusEnum.LOCKED:
          return 'LockIcon'
      }
      return ''
    },
    task () {
      return Task.find(this.taskId)
    },
    status () {
      return this.task?.status || TaskStatusEnum.OPEN
    },
    taskLabelKey () {
      return ['taskStatus', camelCase(this.status)].join('.')
    },
    taskLabel () {
      return this.$t(this.taskLabelKey)
    }
  }
}
</script>

<template>
  <span class="task-status d-flex-inline justify-content-center" :class="classList">
    <component :is="icon" size="1x" />
    {{ taskLabel }}
  </span>
</template>

<style lang="scss" scoped>
  .task-status {
    &--open {
      color: $success;
    }

    &--closed {
      color: $secondary;
    }

    &--locked {
      color: $danger;
    }
  }
</style>
