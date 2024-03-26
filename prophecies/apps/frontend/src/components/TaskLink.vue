<script>
import Task from '@/models/Task'

export default {
  name: 'TaskLink',
  props: {
    taskId: {
      type: [String, Number]
    },
    params: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    task() {
      return Task.query().with('project').whereId(this.taskId).first()
    },
    to() {
      const taskId = this.taskId
      const params = { taskId, ...this.params }
      return { name: 'task-record-review-list', params }
    },
    label() {
      return this.task?.name
    }
  }
}
</script>

<template>
  <router-link :to="to" class="task-link">
    <slot v-bind="{ task }">
      {{ label }}
    </slot>
  </router-link>
</template>
