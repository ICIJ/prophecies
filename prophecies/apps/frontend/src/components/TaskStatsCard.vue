<script>
import moment from 'moment'
import Task, { TaskStatus } from '@/models/Task'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import StatsByRound from '@/components/StatsByRound.vue'

export default {
  name: 'TaskStatsCard',
  components: {
    StatsByRound,
    TaskStatsCardAllRounds

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
      return moment(d).format('ddd DD, MMM YYYY')
    },
    round (value) {
      return Math.round(value)
    }
  },
  computed: {
    celebrate () {
      return this.taskIsDone || this.taskIsClosed
    },
    classList () {
      return this.extended ? 'd-flex flex-row-reverse' : 'd-flex flex-column text-right'
    },
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
    taskIsLocked () {
      return this.task.status === TaskStatus.LOCKED
    },
    taskIsClosed () {
      return this.task.status === TaskStatus.CLOSED
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
      <div class="d-flex justify-content-between ">
        <div class="task-stats-card__heading d-flex flex-column ">
          <h3>
            <router-link
            :to="{
              name: 'task-record-review-list',
              params: { taskId: task.id },
              }"
              class="d-inline-block"
              >
              {{ task.name }}
            </router-link>
            <b-badge class="task-stats-card__heading__project bg-transparent font-weight-normal text-muted">
            {{ task.project.name }}
            </b-badge>
          </h3>
          <p class="pt-2 text-nowrap">
            {{ $tc('taskStatsCard.fullyCheckedItems', taskRecordsCount) }}:
            <span
              class="text-danger font-weight-bold ml-2 task-stats-card__checked"
            >
              {{ taskRecordsDoneCount }} / {{ taskRecordsCount }}
            </span>
          </p>
          <span v-if="extended" class="text-secondary">
              Created at {{ task.created_at | formatDate }}
          </span>
        </div>
         <task-stats-card-all-rounds
              v-if="extended"
                :progress="progress"
                :done="taskRecordsDoneCount"
                :pending="taskRecordsPendingCount"
                class="mx-5 d-none d-lg-block"
          />
        <div class="task-stats-card__status d-flex flex-column justify-content-between text-right" :class="{'task-stats-card__status--extended':extended}">
          <div  :class="{'flex-row-reverse flex-wrap' : extended}">
            <div class="task-stats-card__status__top " :class="{'ml-5 pb-3 ' : extended}">
              <span v-if="taskIsClosed" class="task-stats-card__status__top--closed text-nowrap" >
                {{ $t('taskStatsCard.closed') }}
              <span v-if="extended && celebrate" class="task-stats-card__status--closed ml-2">🎉</span><span class="sr-only">{{taskIsClosed? 'Closed':'Done'}}</span>
              </span>
              <span v-else class="task-stats-card__status__top__priority bg-warning rounded py-1 px-2 text-nowrap">
                {{ $t('taskStatsCard.priority') }} {{ task.priority }}
              </span>
            </div>
            <div  v-if="taskIsLocked"  :class="{' mt-0 py-0' : extended,'py-3':!extended}" >
              <span  class="task-stats-card__status__lock text-danger " >
                <lock-icon size="1.3x" /><span class="sr-only">Unlock</span>
                <span class="task-stats-card__status__lock--locked ml-2 "> {{ $t('taskStatsCard.locked') }}</span>
              </span>
            </div>
            <div v-else-if="!extended && celebrate" class="mt-2 pt-1">
              <span class="task-stats-card__status--closed ml-2">🎉</span><span class="sr-only">{{taskIsClosed? 'Closed':'Done'}}</span>
            </div>
          </div>
          <div v-if="extended" class="task-stats-card__read-tips pt-3 ">
            <router-link :to="{ name: 'tip-list', query: { 'filter[task]': task.id } }" class="btn btn-danger px-3"> Read tips </router-link>
          </div>
        </div>
      </div>

         <task-stats-card-all-rounds
              v-if="extended"
                :progress="progress"
                :done="taskRecordsDoneCount"
                :pending="taskRecordsPendingCount"
                class="mx-auto my-3 d-lg-none"
          />
      <div class="d-flex flex-row flex-grow-1 " :class="{'align-items-center':!extended}">
         <div class=" task-stats-card__progress-by-round d-flex flex-row flex-wrap flex-grow-1 "
              :class="{'mx-auto':extended}"
         >
          <slot name="usersByRound" v-bind:stats="{rounds:task.rounds,progress:progressByRound}">
            <stats-by-round
              v-for="round in task.rounds"
              :key="round"
              :round="round"
              :nbRounds="task.rounds"
              :progress="progressByRound[round]"
            />
          </slot>
         </div>
        <slot name="allRounds" v-if="!extended">
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
        </slot>
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
