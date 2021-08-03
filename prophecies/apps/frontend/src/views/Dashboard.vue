<template>
  <div class="dashboard d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="dashboard__container flex-grow-1">
      <app-header />
      <div class="container-fluid p-5">
        <div class="row">
          <div class="col-4 offset-1">
            <div class="d-flex align-items-center">
              <b-btn-group>
                <b-btn variant="primary" class="font-weight-bold">
                  Team stats
                </b-btn>
                <b-btn variant="outline-primary">
                  Your stats
                </b-btn>
              </b-btn-group>
              <b-dropdown right no-caret variant="link" class="ml-auto">
                <template #button-content>
                  Sort by
                  <chevron-down-icon class="mr-2" />
                </template>
              </b-dropdown>
            </div>
            <app-waiter :for="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
              <task-stats-card :task-id="task.id" v-for="task in tasks" :key="task.id" class="my-5" />
            </app-waiter>
          </div>
          <div class="col-4 offset-2">
            <app-waiter :for="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
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
import { waitFor } from 'vue-wait'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import ProgressCard from '@/components/ProgressCard'
import TaskStatsCard from '@/components/TaskStatsCard'
import Project from '@/models/Project'
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
  async created () {
    await this.waitFor(this.fetchTaskLoader, this.fetchTask)
  },
  computed: {
    tasks () {
      return Task.all()
    },
    fetchTaskLoader () {
      return uniqueId('load-dashboard-task-')
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
