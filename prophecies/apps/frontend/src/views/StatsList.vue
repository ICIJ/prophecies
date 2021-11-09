<template>
  <div class="stats-list d-flex align-items-start">
   <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header reduced />
      <stats-sort-dropdown />
      <div class="container-fluid p-5">
        <div class="col-12">
          <div class="d-flex flex-column">
            <b-form-group>
              <b-form-radio-group
              v-model="teamTaskStats"
              buttons
              button-variant="outline-primary"
              :options="taskStatsOptions" />
            </b-form-group>
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
import { uniqueId } from 'lodash'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'

import TaskStatsCard from '@/components/TaskStatsCard'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'
import Task from '@/models/Task'

import StatsByRound from '@/components/StatsByRound.vue'
import StatsSortDropdown from '@/components/StatsSortDropdown.vue'
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
    StatsSortDropdown
  },
  data () {
    return {
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
    tasks () {
      return Task
        .query()
        .where('taskRecordsCount', (value) => value > 0)
        .get()
        .sort((a, b) => {
          if (a.status === 'CLOSED') {
            return 1
          } else if (b.status === 'CLOSED') {
            return -1
          }
          return 0
        })
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
    }
  }
}
</script>
