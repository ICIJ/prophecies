<template>
  <div class="stats-list d-flex align-items-start">
   <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <div class="col-12">
          <div class="d-flex flex-column">
            <div class="d-flex flex-row justify-content-between">
              <div class="d-flex flex-row align-items-end" >
              <b-form-group >
                <b-form-radio-group
                v-model="teamTaskStats"
                buttons
                button-variant="outline-primary"
                :options="taskStatsOptions" />
              </b-form-group>
              </div>
              <sort-by-dropdown
                :sort.sync="sortField"
                :options="sortOptions"
                class="mb-3 stats-list__sort-by"/>

            </div>
            <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
              <task-stats-card class="my-5"
              v-for="task in tasks"
              :key="task.id"
              :team="teamTaskStats"
              :task-id="task.id" extended>

              <template v-slot:allRounds="{rounds}">
                <task-stats-card-all-rounds
                :progress="rounds.progress"
                :done="rounds.done"
                :pending="rounds.pending"
                />
              </template>

              <template v-slot:usersByRound="{stats}">
                <stats-by-round
                  v-for="(round,index) in stats.rounds"
                  :key="round"
                  :round="index+1"
                  :progress="stats.progress[round]"
                  :choices='choicesByRound[round]'
                  :users='usersByRound[round]'
                  :summary='summaryByRound[round]'
                  extended
                  class="col-4" />
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
import { uniqueId, orderBy, find } from 'lodash'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'

import TaskStatsCard from '@/components/TaskStatsCard'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import Task, { TaskStatusOrder } from '@/models/Task'

import StatsByRound from '@/components/StatsByRound.vue'
import SortByDropdown from '@/components/SortByDropdown.vue'
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
const users = [
  {
    name: 'augie',
    progress: 100,
    done: 5,
    pending: 0
  },
  {
    name: 'marco',
    progress: 0,
    done: 0,
    pending: 20
  },
  {
    name: 'mago',
    progress: 0,
    done: 0,
    pending: 30
  }
]
const usersround2 = [
  {
    name: 'augie',
    progress: 100,
    done: 5,
    pending: 0
  },
  {
    name: 'marco',
    progress: 0,
    done: 0,
    pending: 20
  }
]
const usersround3 = [
  {
    name: 'augie',
    progress: 100,
    done: 5,
    pending: 0
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
    TaskStatsCardAllRounds,
    StatsByRound,
    SortByDropdown
  },
  data () {
    return {
      sortOptions: [
        { value: 'name_asc', label: 'Name (A-Z)', $isDefault: true },
        { value: 'name_desc', label: 'Name (Z-A)' },
        // { value: 'lastReviewed_desc', label: 'Recently reviewed' },
        { value: 'createdAt_desc', label: 'Recently created' },
        { value: 'priority_asc', label: 'Priority (0-9)' },
        { value: 'priority_desc', label: 'Priority (9-0)' },
        { value: 'progress_asc', label: 'Progress (0%-100%)' },
        { value: 'progress_desc', label: 'Progress (100%-0%)' }
      ],
      teamTaskStats: true,
      taskStatsOptions: [
        { text: 'Team stats', value: true },
        { text: 'Your stats', value: false }
      ]
    }
  },
  async created () {
    await this.waitFor(this.fetchTaskLoader, this.fetchTask)
  },
  methods: {
    fetchTask () {
      return Task.api().get()
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
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
      return orderBy(this.unorderedTasks, [this.selectedSortName, this.sortByStatus, 'name'], [this.selectedSortOptionOrder, 'asc', 'asc'])
    },
    selectedSortOption () {
      return find(this.sortOptions, { value: this.sortField })
    },
    selectedSortName () {
      return this.selectedSortOption.value.split('_')[0]
    },
    selectedSortOptionOrder () {
      return this.selectedSortOption.value.split('_')[1]
    },
    sortByStatus () {
      return function (task) {
        return TaskStatusOrder[task.status] === 0
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
    usersByRound () {
      //! TODO API Call stats/:taskId/users OR tasks/taskId/stats/users
      return {
        1: [...users],
        2: [...usersround2],
        3: [...usersround3]
      }
    },
    summaryByRound () {
      //! TODO API Call stats/:taskId OR tasks/taskId/stats
      return {
        1: [...summary],
        2: [...summary],
        3: [...summary]
      }
    },
    fetchTaskLoader () {
      return uniqueId('load-stats-task-')
    },
    sortField: {
      get () {
        const isParamValid = find(this.sortOptions, { value: this.$route.query.sort })
        if (!isParamValid) {
          return 'name_asc'
        } else {
          return this.$route.query.sort
        }
      },
      set (value) {
        const query = { ...this.$route.query, sort: value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    }
  }
}
</script>
<style lang="scss" scoped>
  .stats-list__sort-by  {
      flex:0 1 270px;
  }
</style>
