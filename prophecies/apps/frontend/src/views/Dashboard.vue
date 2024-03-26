<script>
import { uniqueId } from 'lodash'

import { orderTasks } from '@/utils/sort'
import Task, { TaskStatusEnum } from '@/models/Task'
import Tip from '@/models/Tip'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import EmptyPlaceholder from '@/components/EmptyPlaceholder'
import HistoryList from '@/components/HistoryList'
import HistoryFetcher from '@/components/HistoryFetcher'
import LatestTipsCard from '@/components/LatestTipsCard'
import ProgressCard from '@/components/ProgressCard'
import TaskStatsCard from '@/components/TaskStatsCard'

export default {
  name: 'Dashboard',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    LatestTipsCard,
    ProgressCard,
    TaskStatsCard,
    HistoryList,
    HistoryFetcher,
    EmptyPlaceholder
  },
  data() {
    return {
      sortField: 'name_asc',
      teamTaskStats: false
    }
  },
  computed: {
    unorderedTasks() {
      return Task.query()
        .where('taskRecordsCount', (value) => value > 0)
        .where('status', (value) => value !== TaskStatusEnum.CLOSED)
        .get()
    },
    tasks() {
      return orderTasks(this.unorderedTasks)
    },
    tips() {
      return Tip.query().with('project').with('task').orderBy('createdAt', 'desc').get()
    },
    fetchTaskLoader() {
      return uniqueId('load-dashboard-task-')
    },
    taskStatsOptions() {
      return [
        { text: this.$t('statsList.title.yours'), value: false },
        { text: this.$t('statsList.title.team'), value: true }
      ]
    }
  },
  created() {
    return this.setup()
  },
  methods: {
    async setup() {
      await this.waitFor(this.fetchTaskLoader, [this.fetchTask, this.fetchTips])
    },
    fetchTask() {
      return Task.api().get()
    },
    fetchTips() {
      const include = 'project,task'
      const pageSize = '1'
      const sort = '-created_at'
      const params = { include, 'page[size]': pageSize, sort }
      return Tip.api().get('', { params })
    },
    async waitFor(loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map((fn) => fn()))
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
                  <div class="d-flex flex-row justify-content-between">
                    <div class="d-flex flex-row align-items-end">
                      <b-form-group>
                        <b-form-radio-group
                          v-model="teamTaskStats"
                          buttons
                          button-variant="outline-primary"
                          :options="taskStatsOptions"
                        />
                      </b-form-group>
                    </div>
                  </div>
                  <task-stats-card
                    v-for="task in tasks"
                    :key="task.id"
                    class="my-5"
                    :team="teamTaskStats"
                    :task-id="task.id"
                  >
                  </task-stats-card>
                  <div
                    class="dashboard__container__left-panel__stats-link d-flex justify-content-center py-3 mt-3 mb-5"
                  >
                    <router-link class="btn btn-primary font-weight-bold" :to="{ name: 'stats-list' }">{{
                      $t('dashboard.allTasks')
                    }}</router-link>
                  </div>
                </template>
                <div v-else class="card card-body shadow-sm">
                  <empty-placeholder :title="$t('dashboard.noTask')" />
                </div>
              </app-waiter>
            </div>
          </div>
          <div class="col-12 col-xl-6">
            <div class="dashboard__container__right-panel ml-xl-auto">
              <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
                <progress-card v-if="tasks.length" class="mb-5" />
                <latest-tips-card v-if="tips.length" :tips="tips">
                  <template #title>
                    <h2 class="title-dashboard mb-0 font-weight-bold">
                      {{ $t('dashboard.latestTips') }}
                    </h2>
                  </template>
                  <template #itemTitle="slotProps">
                    <p class="tip-item-title-dashboard font-weight-bold">
                      {{ slotProps.tip.name }}
                    </p>
                  </template>
                  <template #footer>
                    <div class="mx-auto">
                      <router-link
                        v-b-tooltip.hover
                        :to="{ name: 'tip-list' }"
                        :title="$t('dashboard.allTips')"
                        class="text-secondary"
                      >
                        {{ $t('dashboard.moreNiceTips') }}
                      </router-link>
                    </div>
                  </template>
                </latest-tips-card>
              </app-waiter>
            </div>
          </div>
        </div>

        <div class="row mt-5 pt-5">
          <history-fetcher v-slot="{ actionIds, isFetching }" class="col-12" :page-size="5">
            <history-list :fluid="false" :limit="5" :fetching="isFetching" :action-ids="actionIds">
              <template #title>
                <span class="text-danger">{{ $t('dashboard.lately') }}</span> in Prophecies
              </template>
              <template #footer>
                <div class="d-flex justify-content-center pt-3">
                  <button class="btn btn-primary border font-weight-bold">
                    <router-link :to="{ name: 'history' }" :title="$t('dashboard.allHistory')" class="text-white">
                      {{ $t('dashboard.showAllHistory') }}
                    </router-link>
                  </button>
                </div>
              </template>
            </history-list>
          </history-fetcher>
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
      &__tasks__sort-by {
        flex: 0 1 200px;
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
        content: '';
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
