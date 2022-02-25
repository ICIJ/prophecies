<template>
  <div class="stats-list d-flex align-items-start">
   <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header hide-nav hide-search/>
      <div class="container-fluid p-5">
        <div class="row">
          <div class="col-12">
            <div class="d-flex flex-wrap justify-content-between">
                <b-form-group class="stats-list__radio d-flex  mr-5">
                  <b-form-radio-group
                  v-model="teamTaskStats"
                  buttons
                  button-variant="outline-primary"
                  :options="taskStatsOptions" />
                </b-form-group>
              <div class="stats-list__filters d-flex align-items-end ">
                <b-form-checkbox class="stats-list__filters__only-open-tasks__checkbox  mb-4 mr-5 pb-1" v-model="onlyOpenTasks">
                  <span class="text-nowrap text-primary">{{$t('statsList.showOnlyOpenTasks')}}</span>
                </b-form-checkbox>
                <task-sort-by-dropdown
                  :sort.sync="sortField"
                  @update:sort-by-cb="updateSortByCallback"
                  class="mb-3 stats-list__filters__sort-by"
                />
              </div>
            </div>
            <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
              <task-stats-card class="stats-list__task-card my-5" v-for="task in tasks" :key="task.id" :task-id="task.id" :team="teamTaskStats" extended>
                <template v-if="fetchTaskUserStatsLoader" v-slot:taskStatsByRound="{stats}" >
                  <stats-by-round
                    v-for="(round,index) in stats.rounds"
                    :key="round"
                    :round="index+1"
                    :progress="stats.progress[round]"
                    :progress-by-user='taskUserStatistics(task.id,round)'
                    :summary='taskUserChoiceStatistics(task.id,round)'
                    extended
                    class="stats-list__task-card__round mx-auto" />
                </template>
              </task-stats-card>
            </app-waiter>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { cloneDeep, uniqueId, filter, orderBy } from 'lodash'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'

import TaskStatsCard from '@/components/TaskStatsCard'
import Task, { TaskStatusEnum, TaskStatusOrder } from '@/models/Task'

import StatsByRound from '@/components/StatsByRound.vue'
import TaskSortByDropdown from '@/components/TaskSortByDropdown.vue'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import User from '@/models/User'

export default {
  name: 'StatsList',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    TaskStatsCard,
    StatsByRound,
    TaskSortByDropdown
  },
  data () {
    return {
      sortField: 'status_asc',
      sortByCb: (tasks) => orderBy(tasks, function (task) {
        return TaskStatusOrder[task.status] === 1
      }),
      teamTaskStats: true,
      taskStatusFilter: true,
      taskStatsOptions: [
        { text: this.$t('statsList.title.team'), value: true },
        { text: this.$t('statsList.title.yours'), value: false }
      ]
    }
  },
  created () {
    return this.setup()
  },
  methods: {
    async setup () {
      await this.waitFor(this.fetchTaskLoader, [this.fetchTask])
      await this.waitFor(this.fetchTaskUserStatsLoader, [this.fetchTaskUserStats, this.fetchTaskUserChoiceStats])
    },
    fetchTask () {
      const params = { include: 'choiceGroup.choices' }
      return Task.api().get('', { params })
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
    updateSortByCallback (cb) {
      this.sortByCb = cb
    },
    taskUserStatistics (taskId, round) {
      let request = TaskUserStatistics.query().with('checker').where('taskId', taskId).where('round', round)
      if (!this.teamTaskStats) {
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
        const cumulate = this.teamTaskStats || (!this.teamTaskStats && this.isMe({ id: checkerStat.checkerId }))
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
    unorderedTasks () {
      return Task
        .query()
        .with('choiceGroup.choices')
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    tasks () {
      const sortedTasks = this.sortByCb(this.unorderedTasks)
      return this.onlyOpenTasks ? filter(sortedTasks, ['status', TaskStatusEnum.OPEN || TaskStatusEnum.LOCKED]) : sortedTasks
    },
    defaultChoicesByTaskId () {
      return this.tasks.reduce((acc, task) => {
        const taskId = task.id
        const choiceGroupId = task.choiceGroupId
        const choices = task.choiceGroup.choices
        const defaultChoices = choices.reduce((prev, choice) =>
          ({ ...prev, [choice.id]: { id: choice.id, name: choice.name, value: choice.value, progress: 0 } }), {})
        acc[taskId] = { [choiceGroupId]: { ...defaultChoices } }
        return acc
      }, {})
    },
    onlyOpenTasks: {
      get () {
        const onlyOpenTasks = this.$route.query.only_open
        if (onlyOpenTasks === 'true') {
          return true
        }
        return false
      },
      set (value) {
        const query = { ...this.$route.query, only_open: !!value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    },
    fetchTaskLoader () {
      return uniqueId('load-stats-task-')
    },
    fetchTaskUserStatsLoader () {
      return uniqueId('load-stats-task-user')
    }
  }
}
</script>
<style lang="scss" scoped>
.stats-list__filters__sort-by
{
  width:240px;
}
</style>
