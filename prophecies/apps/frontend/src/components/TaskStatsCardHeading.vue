<script>
import { formatDate } from '@/utils/date'
import Task from '@/models/Task'

export default {
  name: 'TaskStatsCardHeading',
  filters: {
    formatDate(d) {
      return formatDate(d)
    }
  },
  props: {
    taskId: {
      type: [Number, String]
    },
    taskRecordsCount: {
      type: Number,
      default: 0
    },
    taskRecordsDoneCount: {
      type: Number,
      default: 0
    },
    extended: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    task() {
      return Task.query().with('project').find(this.taskId)
    }
  }
}
</script>

<template>
  <div class="task-stats-card__heading d-flex flex-column justify-content-between">
    <h2>
      <router-link
        :to="{
          name: 'task-record-review-list',
          params: { taskId: task.id }
        }"
        class="d-inline-block"
      >
        {{ task.name }}
      </router-link>
      <b-badge class="task-stats-card__heading__project bg-transparent font-weight-normal text-muted">
        {{ task.project.name }}
      </b-badge>
    </h2>
    <span v-if="taskRecordsCount > 0" class="py-2 text-nowrap">
      {{ $tc('taskStatsCard.fullyCheckedItems', taskRecordsCount) }}:
      <span class="text-danger font-weight-bold ml-2 task-stats-card__checked">
        {{ taskRecordsDoneCount }} / {{ taskRecordsCount }}
      </span>
    </span>
    <span v-else class="py-2 text-nowrap text-secondary">{{ $t('taskStatsCard.noRecordsAssigned') }}</span>
    <span v-if="extended" class="text-secondary pt-2">
      {{ $t('taskStatsCard.createdOn') }} {{ task.created_at | formatDate }}
    </span>
  </div>
</template>

<style lang="scss" scoped>
.task-stats-card__heading {
  flex: 0 1 275px;
}
</style>
