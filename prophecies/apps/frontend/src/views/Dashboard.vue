<template>
  <div class="dashboard d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="dashboard__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <div class="row justify-content-between">
          <div class="col-4">
            <div class="d-flex align-items-center">
              <b-form-group>
                <b-form-radio-group
                  v-model="teamTaskStats"
                  buttons
                  button-variant="outline-primary"
                  :options="taskStatsOptions" />
              </b-form-group>
              <!--b-dropdown right no-caret variant="link" class="ml-auto">
                <template #button-content>
                  Sort by
                  <chevron-down-icon class="mr-2" />
                </template>
              </b-dropdown-->
            </div>
            <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
              <task-stats-card :team="teamTaskStats" :task-id="task.id" v-for="task in tasks" :key="task.id" class="my-5" />
            </app-waiter>
          </div>
          <div class="col-4">
            <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
              <progress-card class="mb-5" />
            </app-waiter>
            <latest-tips-card />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uniqueId } from 'lodash'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import ProgressCard from '@/components/ProgressCard'
import TaskStatsCard from '@/components/TaskStatsCard'
import Task from '@/models/Task'

export default {
  name: 'Dashboard',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    LatestTipsCard,
    ProgressCard,
    TaskStatsCard
  },
  data () {
    return {
      teamTaskStats: true
    }
  },
  async created () {
    await this.waitFor(this.fetchTaskLoader, this.fetchTask)
  },
  computed: {
    tasks () {
      return Task.all()
    },
    fetchTaskLoader () {
      return uniqueId('load-dashboard-task-')
    },
    taskStatsOptions () {
      return [
        { text: 'Team stats', value: true },
        { text: 'Your stats', value: false }
      ]
    }
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
  }
}
</script>
