<script>
import { orderBy } from 'lodash'
import User from '@/models/User'
import Task, { TaskStatusEnum } from '@/models/Task'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import LightDropdown from '@/components/LightDropdown.vue'

const ALL__OPEN_TASKS_ID = '0_all'
export default {
  name: 'UserTaskStatsCard',
  components: {
    TaskStatsCardAllRounds,
    LightDropdown
  },
  props: {
    taskIds: {
      type: Array,
      default: () => []
    },
    userId: {
      type: [String, Number],
      default: undefined
    },
    username: {
      type: String,
      default: undefined
    }
  },
  filters: {
    round (value) {
      return Math.round(value)
    }
  },
  data () {
    return {
      selectedTaskId: ALL__OPEN_TASKS_ID,
      show: false
    }
  },
  created () {
    this.setup()
  },
  computed: {
    user () {
      const id = this.userId ?? this.username
      return User.find(id)
    },
    statsAllOpenTasks () {
      return TaskUserStatistics.query()
        .where('checkerId', this.user.id)
        .where(s => this.openTaskIds.includes(s.taskId))
        .get()
    },
    statsAverageAllStats () {
      const stats = this.getAverage(this.statsAllOpenTasks)
      stats.progress /= (this.openTasks.length ?? 1)
      return stats
    },
    statsAverageByTaskId () {
      return this.openTaskIds.reduce((acc, tId) => {
        acc[tId] = this.getAverageByTaskId(tId)
        return acc
      }, {})
    },
    statsAverageByOption () {
      if (this.selectedTaskId === ALL__OPEN_TASKS_ID) {
        return this.statsAverageAllStats
      }
      return this.statsAverageByTaskId[this.selectedTaskId]
    },
    progressColor () {
      if (this.selectedTaskId === ALL__OPEN_TASKS_ID) {
        return ''
      }
      const task = Task.find(this.selectedTaskId)
      return task.colors[1]
    },
    dropdownTasks () {
      return [{ id: ALL__OPEN_TASKS_ID, name: this.$t('userTaskStatsCard.allOpenTasks') }, ...this.openTasks]
    },
    openTasks () {
      return orderBy(
        Task
          .query()
          .where('status', status => status !== TaskStatusEnum.CLOSED)
          .where('taskRecordsCount', (value) => value > 0)
          .whereIdIn(this.taskIds).get(),
        'name'
      )
    },
    openTaskIds () {
      return this.openTasks.map(t => t.id)
    }
  },
  methods: {
    async setup () {
      await this.fetchTaskUserStats(this.user.id)
    },
    fetchTaskUserStats () {
      const params = { 'filter[checker]': this.user.id }
      return TaskUserStatistics.api().get('', { params })
    },
    counterReducer (acc, s) {
      acc.done += s.doneCount
      acc.pending += s.pendingCount
      acc.progress += s.progress
      return acc
    },
    getAverage (stats) {
      const counters = stats.reduce(this.counterReducer, {
        done: 0,
        pending: 0,
        progress: 0
      })
      if (stats.length) {
        counters.progress /= stats.length
      } else {
        counters.progress = 0
      }
      return counters
    },
    getStatsByTaskId (taskId) {
      return TaskUserStatistics.query()
        .where('checkerId', this.user.id)
        .where('taskId', taskId)
        .get()
    },
    getAverageByTaskId (taskId) {
      const stats = this.statsAllOpenTasks.filter(s => s.taskId === taskId)
      return this.getAverage(stats)
    }
  }
}
</script>

<template>
  <task-stats-card-all-rounds
    class="user-task-stats-card d-flex flex-column mx-auto"
    :done="statsAverageByOption.done"
    :pending="statsAverageByOption.pending"
    :progress="statsAverageByOption.progress"
    :color="progressColor"
  >
    <template #top>
      <div class="d-flex flex-row-reverse py-1">
        <light-dropdown class="user-task-stats-card__dropdown" :items="dropdownTasks" :selected-id.sync="selectedTaskId"/>
      </div>
    </template>
    <template #title> {{ $t('userTaskStatsCard.allRecords') }} </template>
  </task-stats-card-all-rounds>
</template>

<style lang="scss" scoped>
.user-task-stats-card {
  & ::v-deep .task-stats-card-all-rounds {
    width: unset;
    max-width: 360px;
    min-width: unset;
    &__card {
      background-color: white;
    }

    &__all {
      display: flex;
      margin-right: 0.5em;
    }
  }
}
</style>
