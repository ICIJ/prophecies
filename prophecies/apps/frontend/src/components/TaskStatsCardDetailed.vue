<script>
import { cloneDeep, uniqueId } from 'lodash'

import TaskStatsCard from '@/components/TaskStatsCard'

import StatsByRound from '@/components/StatsByRound.vue'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import StatsByUsers from '@/components/StatsByUsers.vue'

import Task from '@/models/Task'

export default {
  name: 'TaskStatsCardDetailed',
  components: {
    TaskStatsCard,
    StatsByRound,
    StatsByUsers
  },
  props: {
    taskId: {
      type: String
    },
    team: {
      type: Boolean,
      required: true
    },
    checkerId: {
      type: String
    }
  },
  created () {
    return this.setup()
  },

  filters: {
    round (value) {
      return Math.round(value)
    }
  },
  methods: {
    setup () {
      return this.waitFor(this.fetchTaskUserStatsLoader, [this.fetchTaskUserStats, this.fetchTaskUserChoiceStats])
    },
    fetchTaskUserStats () {
      const params = { include: 'checker', 'filter[task]': this.taskId }
      return TaskUserStatistics.api().get('', { params })
    },
    fetchTaskUserChoiceStats () {
      const filterChecker = (this.checkerId) ? { 'filter[checker]': this.checkerId } : null
      const params = { include: 'checker,task.choice_group.choices', ...filterChecker }

      return TaskUserChoiceStatistics.api('', { params }).get()
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map(fn => fn()))
      this.$wait.end(loader)
    },
    taskUserStatisticsQuery (round) {
      let request = TaskUserStatistics.query()
        .with('checker')
        .where('taskId', this.taskId)
        .where('round', round)
      if (!this.team && this.checkerId) {
        request = request.where('checkerId', this.checkerId)
      }
      return request.get()
    },
    taskUserChoiceStatisticsQuery (round) {
      let request = TaskUserChoiceStatistics
        .query()
        .where('taskId', this.taskId)
        .with('choice')
        .with('choice.choiceGroup')
        .where('round', round)
      if (!this.team && this.checkerId) {
        request = request.where('checkerId', this.checkerId)
      }
      return request.get()
    },
    summary (round) {
      const stats = this.taskUserChoiceStatisticsQuery(round)

      const defaultTaskChoices = this.defaultChoicesByTaskId[this.taskId]
      const choiceGroups = Object.keys(defaultTaskChoices)
      if (!choiceGroups.length) {
        return []
      }
      const choiceGroupId = choiceGroups[0]
      if (!stats.length) {
        return Object.values(defaultTaskChoices[choiceGroupId])
      }

      const statsAcc = { stats: cloneDeep(defaultTaskChoices), count: 0 }
      const cumulatedStats = stats.reduce((acc, checkerStat) => {
        // check if stat choice group is consistent with task choice group
        const statChoiceGroupId = acc.stats[checkerStat.choice.choiceGroupId]
        if (statChoiceGroupId) {
          statChoiceGroupId[checkerStat.choiceId].progress += checkerStat.count
          acc.count += checkerStat.count
        }
        return acc
      }, statsAcc)

      const statByChoiceGroup = cumulatedStats.stats[choiceGroupId]
      const total = cumulatedStats.count !== 0 ? cumulatedStats.count : 1
      for (const choice in statByChoiceGroup) {
        statByChoiceGroup[choice].progress = statByChoiceGroup[choice].progress * 100 / total
      }
      return Object.values(statByChoiceGroup)
    },
    users (round) {
      return this.taskUserStatisticsQuery(round)
        .map(elem => ({
          name: elem.checker.username,
          pending: elem.pendingCount,
          done: elem.doneCount,
          progress: elem.progress
        }))
    }
  },
  computed: {
    task () {
      return Task.query()
        .with('choiceGroup.choices')
        .find(this.taskId)
    },
    defaultChoicesByTaskId () {
      const acc = {}
      acc[this.taskId] = { }

      if (this.task.choiceGroup) {
        const choiceGroupId = this.task.choiceGroupId
        const choices = this.task.choiceGroup.choices
        const defaultChoices = choices.reduce((prev, choice) =>
          ({ ...prev, [choice.id]: { id: choice.id, name: choice.name, value: choice.value, color: choice.color, progress: 0 } }), {})
        acc[this.taskId][choiceGroupId] = { ...defaultChoices }
        return acc
      }

      return acc
    },
    fetchTaskUserStatsLoader () {
      return uniqueId('load-stats-task-user')
    }
  }
}
</script>

<template>
  <task-stats-card class="stats-list__task-card my-5"
  :task-id="taskId"
  :team="team"
  :checker-id="checkerId" extended>
    <template v-if="fetchTaskUserStatsLoader" v-slot:taskStatsByRound="{stats}" >
      <stats-by-round
        v-for="(round,index) in stats.rounds"
        :key="round"
        :round="index+1"
        :users-stats="users(round)"
        :choice-stats="summary(round)"
        :progress="stats.progress[round]"
        extended
        class="stats-list__task-card__round mx-auto"
        >
        <template #users={users} >
          <stats-by-users :users="users" :with-total="team"/>
        </template>

      </stats-by-round>
    </template>
  </task-stats-card>
</template>
