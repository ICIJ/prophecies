
<script>
import { uniqueId, filter, orderBy } from 'lodash'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'

import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task, { TaskStatusEnum, TaskStatusOrder } from '@/models/Task'

import TaskSortByDropdown from '@/components/TaskSortByDropdown.vue'
import User from '@/models/User'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'

export default {
  name: 'StatsList',
  components: {
    AppHeader,
    AppSidebar,
    AppWaiter,
    TaskStatsCardDetailed,
    TaskSortByDropdown
  },
  data () {
    return {
      sortField: 'status_asc',
      sortByCb: (tasks) => orderBy(tasks, function (task) {
        return TaskStatusOrder[task.status] === 1
      }),
      teamTaskStats: false,
      taskStatusFilter: true,
      taskStatsOptions: [
        { text: this.$t('statsList.title.yours'), value: false },
        { text: this.$t('statsList.title.team'), value: true }
      ]
    }
  },
  created () {
    return this.setup()
  },
  methods: {
    setup () {
      return this.waitFor(this.fetchTaskLoader, [this.fetchTask])
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
    updateSortByCallback (cb) {
      this.sortByCb = cb
    }
  },
  computed: {
    me () {
      return User.me().id
    },
    tasks () {
      return Task
        .query()
        .with('choiceGroup.choices')
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    displayedTasks () {
      const sortedTasks = this.sortByCb(this.tasks)
      return this.onlyOpenTasks ? filter(sortedTasks, ['status', TaskStatusEnum.OPEN || TaskStatusEnum.LOCKED]) : sortedTasks
    },
    onlyOpenTasks: {
      get () {
        return this.$route.query.only_open === 'true'
      },
      set (value) {
        const query = { ...this.$route.query, only_open: !!value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    },
    fetchTaskLoader () {
      return uniqueId('load-stats-task-')
    }
  }
}
</script>

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
              <task-stats-card-detailed
              class="stats-list__task-card my-5"
              v-for="task in displayedTasks" :key="task.id"
              :task-id="task.id"
              :team="teamTaskStats"
              :checker-id="me"/>
            </app-waiter>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.stats-list__filters__sort-by
{
  width:240px;
}
</style>
