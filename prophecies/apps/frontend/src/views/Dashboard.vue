<script>
import { uniqueId, orderBy } from 'lodash'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import ProgressCard from '@/components/ProgressCard'
import TaskStatsCard from '@/components/TaskStatsCard'
import Task, { TaskStatusOrder } from '@/models/Task'
import Tip from '@/models/Tip'
import HistoryList from '@/components/HistoryList.vue'

export default {
  name: 'Dashboard',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    LatestTipsCard,
    ProgressCard,
    TaskStatsCard,
    HistoryList
  },
  data () {
    return {
      sortField: 'name_asc',
      teamTaskStats: true
    }
  },
  async created () {
    await this.waitFor(this.fetchTaskLoader, [this.fetchTask, this.fetchTips])
  },
  computed: {
    unorderedTasks () {
      return Task
        .query()
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    tasks () {
      return orderBy(this.unorderedTasks, [function (task) { return TaskStatusOrder[task.status] === 1 }, 'priority', 'name'])
    },
    tips () {
      return Tip.query()
        .with('project')
        .with('task')
        .orderBy('createdAt', 'desc')
        .get()
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
      return Tip.api().get()
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map(fn => fn()))
      this.$wait.end(loader)
    }
  }
}
</script>

<template>
  <div class="dashboard d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="dashboard__container flex-grow-1">
      <app-header hide-nav />
      <div class="container-fluid p-5">
        <div class="row justify-content-between">
          <div class="col-12 col-xl-6">
            <div class="dashboard__container__left-panel">
              <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
                <template v-if="tasks.length">
                  <div class="d-flex flex-row justify-content-between ">
                    <div class="d-flex flex-row align-items-end" >
                      <b-form-group>
                        <b-form-radio-group
                          v-model="teamTaskStats"
                          buttons
                          button-variant="outline-primary"
                          :options="taskStatsOptions" />
                      </b-form-group>
                    </div>

                  </div>
                  <task-stats-card class="my-5"
                                   v-for="task in tasks"
                                   :key="task.id"
                                   :team="teamTaskStats"
                                   :task-id="task.id" >
                  </task-stats-card>
                  <!-- <div class="d-flex justify-content-center py-3 my-3">
                    <router-link class="btn btn-primary font-weight-bold" :to="{name:'stats-list'}">All stats</router-link>
                  </div> -->
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
                    <h2 class="title-dashboard mb-0 font-weight-bold">
                      Latest tips
                    </h2>
                  </template>
                  <template v-slot:itemTitle="slotProps">
                    <p class="tip-item-title-dashboard font-weight-bold">
                      {{ slotProps.tip.name }}
                    </p>
                  </template>
                  <template v-slot:footer>
                    <div class="mx-auto">
                      <router-link
                        :to="{ name: 'tip-list' }"
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

        <div class="row mt-5 pt-5">

          <div class="col-12">
          <history-list :fluid="false" :limit=5>
            <template v-slot:title>
              <span class="text-danger">Lately</span> in Prophecies
            </template>
            <template v-slot:footer>
              <div class="d-flex justify-content-center pt-3">
                <button class="btn btn-primary border font-weight-bold">
                <router-link
                  :to="{ name: 'history' }"
                  title="All history"
                  class="text-white"
                  >
                  Show me all history
                </router-link>
                </button>
              </div>
            </template>
          </history-list>
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
        &__tasks__sort-by{
          flex:0 1 200px;
        }
      }

      &__right-panel {
        max-width: 460px;
      }

      .tip-item-title-dashboard {
        line-height: 16.94px;
        font-size: 14px;
        color: $body-color;
        margin-bottom: $spacer-lg;
      }

      .title-dashboard {
        position: relative;
        padding-bottom: $spacer;
        color: $primary;

        &:after {
          content: "";
          width: 170%;
          max-width: 115px;
          position: absolute;
          bottom: 0%;
          left: 0;
          height: 7px;
          background: $warning;
          font-weight: 600;
        }
      }
    }
  }
</style>
