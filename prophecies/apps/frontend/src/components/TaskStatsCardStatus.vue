<script>
import moment from 'moment'
import Task, { TaskStatus } from '@/models/Task'

export default {
  name: 'TaskStatsCardStatus',
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
    task () {
      return Task.query().with('project').find(this.taskId)
    },
    taskIsLocked () {
      return this.task.status === TaskStatus.LOCKED
    },
    taskIsClosed () {
      return this.task.status === TaskStatus.CLOSED
    },
    taskIsDone () {
      return this.taskRecordsCount !== 0 ? (this.taskRecordsDoneCount / this.taskRecordsCount) === 1 : false
    }
  }
}
</script>

<template>
  <div class="task-stats-card__status d-flex flex-column justify-content-between text-right" :class="{'task-stats-card__status--extended':extended}">
    <div  class='d-flex flex-column flex-grow-1 justify-content-between '>
      <div class="task-stats-card__status__top " :class="{'ml-5 ' : extended}">
        <span v-if="taskIsClosed" class="task-stats-card__status__top--closed text-nowrap" >
          {{ $t('taskStatsCard.closed') }}
        <span v-if="extended && celebrate" class="task-stats-card__status--closed ml-2">🎉</span><span class="sr-only">{{taskIsClosed? 'Closed':'Done'}}</span>
        </span>
        <span v-else class="task-stats-card__status__top__priority bg-warning rounded py-1 px-2 text-nowrap">
          {{ $t('taskStatsCard.priority') }} {{ task.priority }}
        </span>
      </div>
      <div  v-if="taskIsLocked"  :class="{' mt-0 py-0' : extended,'py-2':!extended}" >
        <span  class="task-stats-card__status__lock text-danger " >
          <lock-icon size="1.3x" /><span class="sr-only">Unlock</span>
          <span class="task-stats-card__status__lock--locked ml-2 "> {{ $t('taskStatsCard.locked') }}</span>
        </span>
      </div>
      <div v-else-if="!extended && celebrate" class="mt-2 pt-1">
        <span class="task-stats-card__status--closed ml-2">🎉</span><span class="sr-only">{{taskIsClosed? 'Closed':'Done'}}</span>
      </div>
    </div>
    <div v-if="extended" class="task-stats-card__read-tips pt-2 ">
      <router-link :to="{ name: 'tip-list', query: { 'filter[task]': task.id } }" class="btn btn-danger px-3"> Read tips </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .task-stats-card {
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
