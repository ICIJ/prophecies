<template>
  <div class="stats-list d-flex align-items-start">
   <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header reduced />
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
              <template #allRounds>
                <TaskStatsCardAllRounds
                :progress="100"
                :round="10"
                :done="10000"
                :pending="10000"
                />
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
export default {
  name: 'StatsList',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    TaskStatsCard,
    TaskStatsCardAllRounds
  },
  props: {

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
    fetchTaskLoader () {
      return uniqueId('load-dashboard-task-')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
