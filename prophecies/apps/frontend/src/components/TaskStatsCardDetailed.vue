<template>
  <task-stats-card class="stats-list__task-card my-5" :task-id="taskId" :team="team" extended>
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

<script>
import { cloneDeep, uniqueId } from 'lodash'

import TaskStatsCard from '@/components/TaskStatsCard'

import StatsByRound from '@/components/StatsByRound.vue'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import User from '@/models/User'
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
    team: {
      type: Boolean
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
      return TaskUserChoiceStatistics.api().get()
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map(fn => fn()))
      this.$wait.end(loader)
    },
    isMe ({ id = null } = {}) {
      return id === User.me().id
    },
    taskUserStatistics (taskId, round) {
      let request = TaskUserStatistics.query().with('checker').where('taskId', taskId).where('round', round)
      if (!this.team) {
        request = request.where('checkerId', User.me().id)
      }
      return request.get()
    },
    taskUserChoiceStatistics (taskId, round) {
      const stats = TaskUserChoiceStatistics.query().where('taskId', taskId).with('choice').where('round', round).get()
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
        const cumulate = this.team || (!this.team && this.isMe({ id: checkerStat.checkerId }))
        // check if stat choice group is consistent with task choice group
        const statChoiceGroupId = acc.stats[checkerStat.choice.choiceGroupId]
        if (cumulate && statChoiceGroupId) {
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
