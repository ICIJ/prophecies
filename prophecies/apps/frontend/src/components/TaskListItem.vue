<script>
import Task from '@/models/Task'
import TaskLink from '@/components/TaskLink'
import TaskStatus from '@/components/TaskStatus'

export default {
  name: 'TaskListItem',
  components: {
    TaskLink,
    TaskStatus
  },
  props: {
    taskId: {
      type: [String, Number]
    },
    params: {
      type: Object,
      default: () => ({})
    },
    noProject: {
      type: Boolean
    },
    noStatus: {
      type: Boolean
    }
  },
  computed: {
    task() {
      return Task.query().with('project').whereId(this.taskId).first()
    },
    project() {
      return this.task.project
    }
  }
}
</script>

<template>
  <span v-if="task" class="task-list-item">
    <task-link :task-id="taskId" :params="params" class="task-list-item__link font-weight-bold" />
    <span v-if="!noProject" class="task-list-item__project"> in {{ project.name }} </span>
    <task-status v-if="!noStatus" class="task-list-item__status ml-2" :task-id="taskId" />
  </span>
</template>
