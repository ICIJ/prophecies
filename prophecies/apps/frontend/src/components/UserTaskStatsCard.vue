<script>
import { find, orderBy } from 'lodash'
import User from '@/models/User'
import Task from '@/models/Task'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import { directive as onClickaway } from 'vue-clickaway'

const ALL__OPEN_TASKS_ID = '0_all'
export default {
  name: 'UserTaskStatsCard',
  components: {
    TaskStatsCardAllRounds
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
  directives: {
    onClickaway
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
      stats.progress /= this.openTasks.length
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
    selectedTask () {
      return find(this.dropdownTasks, { id: this.selectedTaskId })
    },
    dropdownTasks () {
      return [{ id: ALL__OPEN_TASKS_ID, name: this.$t('userTaskStatsCard.allOpenTasks') }, ...this.openTasks]
    },
    openTasks () {
      return orderBy(
        Task.query().where('status', 'OPEN').whereIdIn(this.taskIds).get(),
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
      counters.progress = stats.length
        ? (counters.progress /= stats.length)
        : 0
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
    },
    toggle () {
      this.show = !this.show
    },
    close () {
      this.show = false
    },
    select (e) {
      this.selectedTaskId = e.target.dataset.taskid
    },
    isActive (taskId) {
      return this.selectedTaskId === taskId
    }
  }
}
</script>

<template>
  <task-stats-card-all-rounds
    class="user-task-stats-card"
    :done="statsAverageByOption.done"
    :pending="statsAverageByOption.pending"
    :progress="statsAverageByOption.progress"
  >
    <template #top>
      <div class="d-flex flex-row-reverse py-1">
        <div
          class="user-task-stats-card__dropdown dropdown"
          :class="{ show: show }"
        >
          <span
            class="user-task-stats-card__dropdown__selected text-primary dropdown-toggle font-weight-bold text-primary"
            type="button"
            id="dropdownMenuButton"
            v-on-clickaway="close"
            @click="toggle"
            aria-haspopup="true"
            aria-expanded="false"
          >
            {{ selectedTask.name }}
          </span>
          <ul
            class="user-task-stats-card__dropdown__options dropdown-menu dropdown-menu-right"
            :class="{ show: show }"
            aria-labelledby="dropdownMenuButton"
          >
            <li
              v-for="task in dropdownTasks"
              :key="task.id"
              @click="select"
              class="dropdown-item"
              :class="{ active: isActive(task.id) }"
              :data-taskid="task.id"
            >
              {{ task.name }}
            </li>
          </ul>
        </div>
      </div>
    </template>
    <template #title> {{ $t('userTaskStatsCard.allRecords') }} </template>
  </task-stats-card-all-rounds>
</template>

<style lang="scss" scoped>
.user-task-stats-card {
  & /deep/ .task-stats-card-all-rounds {
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
