<script>
import { cloneDeep, uniqueId } from 'lodash'

import TaskStatsCard from '@/components/TaskStatsCard'

import StatsByRound from '@/components/StatsByRound.vue'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import Task from '@/models/Task'

export default {
  name: 'TaskStatsCardDetailed',
  components: {
    TaskStatsCard,
    StatsByRound
  },
  props: {
    taskId: {
      type: String
    },
    checkerId: {
      type: String
    }
  },
  created () {
    return this.setup()
  },
  methods: {
    setup () {
      return this.waitFor(this.fetchTaskUserStatsLoader, [this.fetchTaskUserStats, this.fetchTaskUserChoiceStats])
    },
    fetchTaskUserStats () {
      return TaskUserStatistics.api().get()
    },
    fetchTaskUserChoiceStats () {
      const filterChecker = this.checkerId ? { 'filter[checker]': this.checkerId } : null
      const params = { include: 'checker,task.choice_group.choices', ...filterChecker }

      return TaskUserChoiceStatistics.api('', { params }).get()
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map(fn => fn()))
      this.$wait.end(loader)
    },
    taskUserStatistics (taskId, round) {
      let request = TaskUserStatistics.query().with('checker').where('taskId', taskId).where('round', round)
      if (this.checkerId) {
        request = request.where('checkerId', this.checkerId)
      }
      return request.get()
    },
    taskUserChoiceStatistics (taskId, round) {
      let request = TaskUserChoiceStatistics
        .query()
        .where('taskId', taskId)
        .with('choice')
        .with('choice.choiceGroup')
        .where('round', round)
      if (this.checkerId) {
        request = request.where('checkerId', this.checkerId)
      }
      const stats = request.get()

      const defaultTaskChoices = this.defaultChoicesByTaskId[taskId]
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
    }
  },
  computed: {
    task () {
      return Task.query()
        .with('choiceGroup.choices').whereId(this.taskId).first()
    },
    defaultChoicesByTaskId () {
      const choiceGroupId = this.task.choiceGroupId
      const choices = this.task.choiceGroup.choices
      const defaultChoices = choices.reduce((prev, choice) =>
        ({ ...prev, [choice.id]: { id: choice.id, name: choice.name, value: choice.value, progress: 0 } }), {})
      const acc = {}
      acc[this.taskId] = { [choiceGroupId]: { ...defaultChoices } }
      return acc
    },
    fetchTaskUserStatsLoader () {
      return uniqueId('load-stats-task-user')
    }
  }
}
</script>

<template>
  <task-stats-card class="stats-list__task-card my-5" :task-id="taskId" :team="checkerId!==undefined" extended>
    <template v-if="fetchTaskUserStatsLoader" v-slot:taskStatsByRound="{stats}" >
      <stats-by-round
        v-for="(round,index) in stats.rounds"
        :key="round"
        :round="index+1"
        :progress="stats.progress[round]"
        :progress-by-user='taskUserStatistics(taskId,round)'
        :summary='taskUserChoiceStatistics(taskId,round)'
        extended
        class="stats-list__task-card__round mx-auto" />
    </template>
  </task-stats-card>
</template>
