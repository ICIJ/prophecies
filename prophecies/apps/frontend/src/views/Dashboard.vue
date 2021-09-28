<script>
import { uniqueId } from 'lodash'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import ProgressCard from '@/components/ProgressCard'
import TaskStatsCard from '@/components/TaskStatsCard'
import Task from '@/models/Task'
import Tip from '@/models/Tip'

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
    await this.waitFor(this.fetchTaskLoader, this.fetchTask, this.fetchTips)
  },
  computed: {
    tasks () {
      return Task
        .query()
        .where('taskRecordsCount', (value) => value > 0)
        .get()
        .sort((a,b)=>{
          if(a.status === "CLOSED"){
            return 1
          }else if(b.status === "CLOSED"){
            return -1
          }
          return 0
      })
    },
    tips () {
      return Tip.all()
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
    fetchTips () {
      return Tip.api().get('', {})
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    }
  }
}
</script>

<template>
  <div class="dashboard d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="dashboard__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <div class="row justify-content-between">
          <div class="col-12 col-xl-6">
            <div class="dashboard__container__left-panel">
              <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
                <template v-if="tasks.length">
                  <div class="d-flex align-items-center">
                    <b-form-group>
                      <b-form-radio-group
                        v-model="teamTaskStats"
                        buttons
                        button-variant="outline-primary"
                        :options="taskStatsOptions" />
                    </b-form-group>
                  </div>
                  <task-stats-card class="my-5"
                                   v-for="task in tasks"
                                   :key="task.id"
                                   :team="teamTaskStats"
                                   :task-id="task.id" />
                </template>
                <div v-else class="card card-body shadow-sm text-center text-muted text-small">
                  No tasks yet.
                </div>
              </app-waiter>
            </div>
          </div>
          <div class="col-12 col-xl-6">
            <div class="dashboard__container__right-panel ml-xl-auto">
              <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
                <progress-card class="mb-5" v-if="tasks.length" />
                <latest-tips-card :tips="tips">
                  <template v-slot:title>
                    <h2 class="latest-tips-card__title text-primary mb-0 font-weight-bold">
                      Latest tips
                    </h2>
                  </template>
                  <template v-slot:footer>
                    <div class="mx-auto">
                      <router-link
                        :to="{ name: 'tip-list', params: {} }"
                        title="All tips"
                        v-b-tooltip.hover
                        class="text-secondary">
                        More nice tips
                      </router-link>
                    </div>
                  </template>
                </latest-tips-card>
              </app-waiter>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .dashboard {
    &__container {
        &__left-panel {
          max-width: 460px;
        }

        &__right-panel {
          max-width: 460px;
        }
    }
  }
</style>
