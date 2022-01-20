<script>
import { camelCase, kebabCase } from 'lodash'
import Task, { TaskStatus } from '@/models/Task'

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
        case TaskStatus.OPEN:
          return 'CheckIcon'
        case TaskStatus.LOCKED:
          return 'LockIcon'
      }
    },
    task () {
      return Task.find(this.taskId)
    },
    status () {
      return this.task?.status || TaskStatus.OPEN
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