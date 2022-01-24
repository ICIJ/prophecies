<script>
import { formatDate } from '@/utils/date'
import Task, { TaskStatusEnum } from '@/models/Task'
import TaskStatus from '@/components/TaskStatus.vue'
import { camelCase } from 'lodash'
export default {
  components: { TaskStatus },
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
      return formatDate(d)
    },
    round (value) {
      return Math.round(value)
    }
  },
  computed: {
    celebrate () {
      return this.taskIsDone || this.task.close
    },
    task () {
      return Task.query().with('project').find(this.taskId)
    },
    taskIsDone () {
      return this.taskRecordsCount !== 0 ? (this.taskRecordsDoneCount / this.taskRecordsCount) === 1 : false
    },

    status () {
      if (this.task.open && this.taskIsDone) {
        return 'DONE'
      }

      return this.task?.status || TaskStatusEnum.OPEN
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
  <div class="task-stats-card__status d-flex flex-column justify-content-between text-right" :class="{'task-stats-card__status--extended':extended}">
    <div  class='d-flex flex-column flex-grow-1 justify-content-between '>
      <div class="task-stats-card__status__top " :class="{'ml-5 ' : extended}">
        <template v-if="task.close">
          <task-status :task-id="task.id" class="ml-2" />
          <template v-if="extended && celebrate"><span class="ml-2">🎉</span><span class="sr-only">{{taskLabel}}</span></template>
        </template>
        <span v-else class="task-stats-card__status__top__priority bg-warning rounded py-1 px-2 text-nowrap">
          {{ $t('taskStatsCard.priority') }} {{ task.priority }}
        </span>
      </div>
      <div  v-if="task.locked"  :class="{'mt-0 py-0' : extended,'py-2':!extended}" >
          <task-status :task-id="task.id" class="ml-2" />
      </div>
      <div v-else-if="!extended && celebrate" class="py-2 mb-1">
        <span class="ml-2">🎉</span><span class="sr-only">{{taskLabel}}</span>
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

    }

  }
</style>
