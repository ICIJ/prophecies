<template>
  <div class="task-stats-card card card-body shadow-sm d-flex">
    <div></div>
    <div>
      <div class="d-flex align-items-center mb-3 task-stats-card__heading">
        <h3 class="m-0">
          <router-link :to="{ name: 'task-record-reviews', params: { taskId: task.id } }">
            {{ task.name }}
          </router-link>
          <b-badge class="task-stats-card__heading__project bg-transparent font-weight-normal text-muted">
            {{ task.project.name }}
          </b-badge>
        </h3>
        <span class="bg-warning rounded py-1 px-2 ml-auto task-stats-card__heading__priority">
          Priority {{ task.priority }}
        </span>
      </div>
      <p>
        Fully checked items:
        <span class="text-danger font-weight-bold ml-2 task-stats-card__checked">
          {{ taskRecordsDoneCount }} / {{ taskRecordsCount }}
        </span>
      </p>
      <div class="d-flex align-items-center">
        <ul class="task-stats-card__progress-by-round list-inline m-0">
          <li class="task-stats-card__progress-by-round__item list-inline-item" v-for="round in task.rounds" :key="round">
            Round {{ round }}
            <span class="task-stats-card__progress-by-round__item__value font-weight-bold ml-3">
              {{ progressByRound[round] | round }}%
            </span>
            <span class="text-muted mx-2" v-if="round !== task.rounds">
              |
            </span>
          </li>
        </ul>
        <span class="task-stats-card__progress bg-primary text-white font-weight-bold rounded py-1 px-2 ml-auto">
          {{ progress | round }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import Task from '@/models/Task'

export default {
  name: 'TaskStatsCard',
  props: {
    taskId: {
      type: [Number, String]
    },
    team: {
      type: Boolean
    }
  },
  filters: {
    round (value) {
      return Math.round(value)
    }
  },
  computed: {
    task () {
      return Task
        .query()
        .with('project')
        .find(this.taskId)
    },
    taskRecordsCount () {
      if (this.team) {
        return this.task.taskRecordsCount
      }
      return this.task.userTaskRecordsCount
    },
    taskRecordsDoneCount () {
      if (this.team) {
        return this.task.taskRecordsDoneCount
      }
      return this.task.userTaskRecordsDoneCount
    },
    progress () {
      if (this.team) {
        return this.task.progress
      }
      return this.task.userProgress
    },
    progressByRound () {
      if (this.team) {
        return this.task.progressByRound
      }
      return this.task.userProgressByRound
    }
  }
}
</script>
