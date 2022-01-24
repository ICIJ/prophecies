<script>
import { formatDate } from '@/utils/date'
import Task from '@/models/Task'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import TaskStatsCardHeading from '@/components/TaskStatsCardHeading.vue'
import TaskStatsCardStatus from './TaskStatsCardStatus.vue'
import StatsByRound from '@/components/StatsByRound.vue'

export default {
  name: 'TaskStatsCard',
  components: {
    TaskStatsCardAllRounds,
    StatsByRound,
    TaskStatsCardHeading,
    TaskStatsCardStatus
  },
  props: {
    taskId: {
      type: [Number, String]
    },
    team: {
      type: Boolean
    },
    extended: {
      type: Boolean,
      default: false
    }
  },
  filters: {
    formatDate (d) {
      return formatDate(d)
    },
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
    taskRecordsPendingCount () {
      return this.taskRecordsCount - this.taskRecordsDoneCount
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

<template>
    <div class="task-stats-card card card-body shadow-sm d-flex">
      <div class="d-flex justify-content-between ">
        <task-stats-card-heading
          :extended="extended"
          :taskId="task.id"
          :taskRecordsDoneCount="taskRecordsDoneCount"
          :taskRecordsCount="taskRecordsCount"
        />
        <task-stats-card-all-rounds
          v-if="extended"
          :progress="progress"
          :done="taskRecordsDoneCount"
          :pending="taskRecordsPendingCount"
          class="mx-5 d-none d-lg-block"
        />
        <task-stats-card-status
          :extended="extended"
          :taskId="task.id"
          :taskRecordsDoneCount="taskRecordsDoneCount"
          :taskRecordsCount="taskRecordsCount"
        />
      </div>
      <task-stats-card-all-rounds
            v-if="extended"
            :progress="progress"
            :done="taskRecordsDoneCount"
            :pending="taskRecordsPendingCount"
            class="mx-auto my-3 d-lg-none"
      />
      <div v-if="extended" class="d-flex flex-row flex-grow-1 pt-2">
         <div class=" task-stats-card__progress-by-round d-flex flex-row flex-wrap flex-grow-1 mx-auto">
          <slot name="taskStatsByRound" v-bind:stats="{rounds:task.rounds,progress:progressByRound}" />
         </div>
      </div>
      <div v-else class="d-flex flex-row flex-grow-1 pt-2 align-items-center">
         <div class=" task-stats-card__progress-by-round d-flex flex-row flex-wrap flex-grow-1 ">
            <stats-by-round
              v-for="round in task.rounds"
              :key="round"
              :round="round"
              :nbRounds="task.rounds"
              :progress="progressByRound[round]"
            />
         </div>
          <span class="task-stats-card__progress bg-primary text-white font-weight-bold rounded py-1 px-2 ml-auto">
            {{ progress | round }}%
          </span>
      </div>
    </div>
</template>

<style lang="scss" scoped>
  .task-stats-card {
    &__heading {
      flex: 0 1 275px
    }
    &__status{
      &--extended {
        flex: 0 1 275px
      }
      &__top{

        &--closed  {
          color: $secondary;
        }

      }

    }

  }
</style>
