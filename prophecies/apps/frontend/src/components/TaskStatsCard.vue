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
      return Task.query().with('project').find(this.taskId)
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
    taskIsLocked () {
      return this.task.status === 'LOCKED'
    },
    taskIsClosed () {
      return this.task.status === 'CLOSED'
    },
    taskIsDone () {
      return this.taskRecordsCount !== 0 ? (this.taskRecordsDoneCount / this.taskRecordsCount) === 1 : false
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

<template>
  <div class="task-stats-card card card-body shadow-sm d-flex">
    <div></div>
    <div>
      <div class="d-flex align-items-center mb-3 task-stats-card__heading">
        <h3 class="m-0">
          <router-link
            :to="{
              name: 'task-record-review-list',
              params: { taskId: task.id },
            }"
            class="d-inline-block"
          >
            {{ task.name }}
          </router-link>
          <b-badge
            class="
              task-stats-card__heading__project
              bg-transparent
              font-weight-normal
              text-muted
            "
          >
            {{ task.project.name }}
          </b-badge>
        </h3>
        <span v-if="taskIsClosed" class="ml-auto task-stats-card__heading--closed" >
          {{ $t('taskStatsCard.closed') }}
        </span>
        <span v-else class=" bg-warning rounded ml-auto py-1 px-2  task-stats-card__heading__priority">
          {{ $t('taskStatsCard.priority') }} {{ task.priority }}
        </span>
      </div>
      <div class="d-flex align-items-center">
        <p>
          {{ $tc('taskStatsCard.fullyCheckedItems', taskRecordsCount) }}:
          <span
            class="text-danger font-weight-bold ml-2 task-stats-card__checked"
          >
            {{ taskRecordsDoneCount }} / {{ taskRecordsCount }}
          </span>
        </p>
        <p class="ml-auto d-flex text-danger" v-if="taskIsLocked">
          <lock-icon size="1.5x" /><span class="sr-only">Unlock</span>
          <span class="task-stats-card__status--locked ml-2"> {{ $t('taskStatsCard.locked') }}</span>
        </p>
        <p class="ml-auto d-flex" v-else-if="taskIsDone || taskIsClosed">
          <span class="task-stats-card__status--closed ml-2">🎉</span><span class="sr-only">Closed</span>
        </p>
      </div>
      <div class="d-flex align-items-center">
        <ul class="task-stats-card__progress-by-round list-inline m-0">
          <li
            class="task-stats-card__progress-by-round__item list-inline-item"
            v-for="round in task.rounds"
            :key="round"
          >
            {{ $t('taskStatsCard.round') }} {{ round }}
            <span
              class="
                task-stats-card__progress-by-round__item__value
                font-weight-bold
                ml-3
              "
            >
              {{ progressByRound[round] | round }}%
            </span>
            <span class="text-muted mx-2" v-if="round !== task.rounds">
              |
            </span>
          </li>
        </ul>
        <span
          class="
            task-stats-card__progress
            bg-primary
            text-white
            font-weight-bold
            rounded
            py-1
            px-2
            ml-auto
          "
        >
          {{ progress | round }}%
        </span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .task-stats-card {

    &__heading{

      &--closed  {
        color: $secondary;
      }
    }
  }
</style>
