<template>
  <div class="task-stats-card card card-body shadow d-flex">
    <div></div>
    <div>
      <div class="d-flex align-items-center mb-3 task-stats-card__heading">
        <h3 class="m-0">
          {{ task.name }}
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
          {{ task_records_done_count }} / {{ task_records_count }}
        </span>
      </p>
      <div class="d-flex align-items-center">
        <ul class="task-stats-card__progress-by-round list-inline m-0">
          <li class="task-stats-card__progress-by-round__item list-inline-item" v-for="round in task.rounds" :key="round">
            Round {{ round }}
            <span class="task-stats-card__progress-by-round__item__value font-weight-bold ml-3">
              {{ progress_by_round[round] | round }}%
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
  name: 'StatsCard',
  props: {
    taskId: {
      type: Number
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
        .with('choice_group')
        .find(this.taskId)
    },
    task_records_count () {
      if (this.team) {
        return this.task.task_records_count
      }
      return this.task.user_task_records_count
    },
    task_records_done_count () {
      if (this.team) {
        return this.task.task_records_done_count
      }
      return this.task.user_task_records_done_count
    },
    progress () {
      if (this.team) {
        return this.task.progress
      }
      return this.task.user_progress
    },
    progress_by_round () {
      if (this.team) {
        return this.task.progress_by_round
      }
      return this.task.user_progress_by_round
    }
  }
}
</script>
