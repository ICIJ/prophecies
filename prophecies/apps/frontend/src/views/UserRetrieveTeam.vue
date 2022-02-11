<script>
import { formatDateLongAlt } from '@/utils/date'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import UserCard from '@/components/UserCard'
import Task from '@/models/Task'
import User from '@/models/User'
import TaskUserStatistics from '@/models/TaskUserStatistics'

export default {
  name: 'UserRetrieveTeam',
  components: {
    UserCard,
    TaskStatsCardAllRounds
  },
  props: {
    username: {
      type: String
    }
  },
  filters: {
    formatDate (d) {
      return formatDateLongAlt(d)
    },
    isTaskOpen (taskId) {
      return Task.find(taskId)?.open
    }
  },
  data () {
    return {
      teammates: []
    }
  },
  created () {
    this.setup()
  },
  computed: {
    user () {
      return User.find(this.username)
    },
    teammateStats () {
      return this.teammates.reduce((acc, tm) => {
        acc[tm.id] = acc[tm.id] || {}
        acc[tm.id] = this.statsByUserId(tm.id)
        return acc
      }, {})
    }
  },
  methods: {
    async setup () {
      const tms = await this.fetchUserTasks()
      const promises = tms.map(t => {
        return this.fetchTaskUserStats(t.id)
      })
      await Promise.all(promises)
      this.teammates = tms
    },
    reducer (acc, s) {
      acc.done += s.doneCount
      acc.pending += s.pendingCount
      acc.progress += s.progress
      return acc
    },
    getStatAvg (stats) {
      const reduced = stats.reduce(this.reducer, { done: 0, pending: 0, progress: 0 })
      reduced.progress = stats.length ? reduced.progress /= stats.length : 0
      return reduced
    },
    statsByUserId (userId) {
      return this.getStatAvg(TaskUserStatistics.query().where('checkerId', userId).get())
    },
    async fetchUserTasks () {
      const params = { 'filter[checkers]': this.user.id, include: 'project,checkers' }
      const { entities: { User: users } } = await Task.api().get('', { params })
      return users.filter(u => u.id !== this.user.id)
    },
    fetchTaskUserStats (userId) {
      const params = { 'filter[checker]': userId }
      return TaskUserStatistics.api().get('', { params })
    }
  }
}
</script>

<template>
  <div class="user-retrieve-team container-fluid">
    <div class="row">
      <div
        class="col-12 col-xl-6 mb-4"
        v-for="{ id } in teammates"
        :key="id"
      >
        <user-card class="user-retrieve-team__user-card h-100" :user-id="id" background>
          <template #footer >
            <task-stats-card-all-rounds
            :done='teammateStats[id].done'
            :pending='teammateStats[id].pending'
            :progress='teammateStats[id].progress'
            >
              <template #title >
                All records
              </template>
            </task-stats-card-all-rounds>
          </template>
        </user-card>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .user-retrieve-team  {
    & /deep/ .user-card__assigned-tasks__list{
      height: 5rem;
      overflow-y: auto;
    }

    & /deep/ .task-stats-card-all-rounds{
      background-color: white;
      padding-left: 2.5em;
      padding-right: 3em;
      width: unset;
      min-width: unset;
      max-width: 360px;

      &__all{
        display:flex;
        margin-right:0.5em ;
      }

    }
  }
</style>