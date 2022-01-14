<template>
  <div class="stats-list d-flex align-items-start">
   <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <div class="col-12">
          <div class="d-flex flex-wrap justify-content-between">
              <b-form-group class="stats-list__radio d-flex align-items-end mr-5">
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
            <task-stats-card class="my-5"
            v-for="task in tasks"
            :key="task.id"
            :team="teamTaskStats"
            :task-id="task.id" extended>

              <template v-slot:usersByRound="{stats}">
                 <stats-by-round
                  v-for="(round,index) in stats.rounds"
                  :key="round"
                  :round="index+1"
                  :progress="stats.progress[round]"
                  :choices='choicesByRound[round]'
                  :progress-by-user-ids='taskUserStatistics(task.id,round)'
                  :summary='summaryByRound[round]'
                  extended
                  class=" mx-auto " />
              </template>
            </task-stats-card>

          </app-waiter>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uniqueId, filter, orderBy } from 'lodash'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'

import TaskStatsCard from '@/components/TaskStatsCard'
import Task, { TaskStatus, TaskStatusOrder } from '@/models/Task'

import StatsByRound from '@/components/StatsByRound.vue'
import TaskSortByDropdown from '@/components/TaskSortByDropdown.vue'
import TaskUserStatistics from '@/models/TaskUserStatistics'
const choices = [
  {
    value: 'correct',
    name: 'Correct',
    progress: 100
  },
  {
    value: 'incorrect',
    name: 'Incorrect',
    progress: 100
  },
  {
    value: 'dontknow',
    name: 'Dont know',
    progress: 100
  }
]

const summary = [
  {
    name: 'C',
    value: 95
  },
  {
    name: 'I',
    value: 1
  },
  {
    name: 'D',
    value: 4
  }
]

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
        { text: 'Team stats', value: true },
        { text: 'Your stats', value: false }
      ]
    }
  },
  async created () {
    await this.waitFor(this.fetchTaskLoader, [this.fetchTask, this.fetchTaskUserStats])
  },
  methods: {
    fetchTask () {
      return Task.api().get()
    },
    fetchTaskUserStats () {
      return TaskUserStatistics.api().get()
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map(fn => fn()))
      this.$wait.end(loader)
    },
    updateSortByCallback (cb) {
      this.sortByCb = cb
    },
    taskUserStatistics (taskId, round) {
      return TaskUserStatistics.query().with('checker').where('taskId', taskId).where('round', round).get()
    }
  },
  computed: {
    unorderedTasks () {
      return Task
        .query()
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    tasks () {
      const sortedTasks = this.sortByCb(this.unorderedTasks)
      return this.onlyOpenTasks ? filter(sortedTasks, ['status', TaskStatus.OPEN || TaskStatus.LOCKED]) : sortedTasks
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
    choicesByRound () {
      //! TODO API Call stats/:taskId OR tasks/taskId/stats
      return {
        1: [...choices],
        2: [...choices],
        3: [...choices]
      }
    },
    summaryByRound (taskId) {
      //! TODO API Call stats/:taskId OR tasks/taskId/stats
      return {
        1: [...summary],
        2: [...summary],
        3: [...summary]
      }
    },
    fetchTaskLoader () {
      return uniqueId('load-stats-task-')
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
