<script>
import { uniqueId, filter, orderBy } from 'lodash'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task, { TaskStatusEnum, TaskStatusOrder } from '@/models/Task'
import TaskSortByDropdown from '@/components/TaskSortByDropdown'
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
  data() {
    return {
      sortField: 'status_asc',
      sortByCb: (tasks) =>
        orderBy(tasks, function (task) {
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
  computed: {
    me() {
      return User.me().id
    },
    tasks() {
      return Task.query()
        .with('choiceGroup.choices')
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    displayedTasks() {
      const sortedTasks = this.sortByCb(this.tasks)
      const onlyOpenTasks = this.onlyOpenTasks
        ? filter(sortedTasks, ['status', TaskStatusEnum.OPEN || TaskStatusEnum.LOCKED])
        : sortedTasks
      const onlyForMe = this.tasksWithRecordsLeftForMe
        ? onlyOpenTasks.filter((t) => t.userTaskRecordsCount - t.userTaskRecordsDoneCount > 0)
        : onlyOpenTasks
      return onlyForMe
    },
    onlyOpenTasks: {
      get() {
        return this.$route.query.only_open === 'true'
      },
      set(value) {
        const query = { ...this.$route.query, only_open: !!value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    },
    tasksWithRecordsLeftForMe: {
      get() {
        return this.$route.query.only_for_me === 'true'
      },
      set(value) {
        const query = { ...this.$route.query, only_for_me: !!value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    },
    fetchTaskLoader() {
      return uniqueId('load-stats-task-')
    }
  },
  created() {
    return this.setup()
  },
  methods: {
    setup() {
      return this.waitFor(this.fetchTaskLoader, [this.fetchTask])
    },
    fetchTask() {
      const params = { include: 'choiceGroup.choices' }
      return Task.api().get('', { params })
    },
    fetchTaskUserStats() {
      return TaskUserStatistics.api().get()
    },
    fetchTaskUserChoiceStats() {
      return TaskUserChoiceStatistics.api().get()
    },
    async waitFor(loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map((fn) => fn()))
      this.$wait.end(loader)
    },
    updateSortByCallback(cb) {
      this.sortByCb = cb
    }
  }
}
</script>

<template>
  <div class="stats-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header hide-nav hide-search />
      <div class="container-fluid p-5">
        <div class="row">
          <div class="col-12">
            <div class="d-flex flex-wrap justify-content-between">
              <b-form-group class="stats-list__radio d-flex mr-5 mr-auto">
                <b-form-radio-group
                  v-model="teamTaskStats"
                  buttons
                  button-variant="outline-primary"
                  :options="taskStatsOptions"
                />
              </b-form-group>

              <div class="d-flex align-items-lg-end align-items-center justify-content-end flex-grow-1 mt-2 mt-lg-0">
                <div class="d-flex flex-lg-row flex-column my-auto">
                  <label class="text-nowrap text-primary mr-4">{{ $t('statsList.showOnly') }} </label>
                  <b-form-checkbox
                    id="tasksForMe"
                    v-model="tasksWithRecordsLeftForMe"
                    class="stats-list__filters__checkbox--tasks-for-me mr-4"
                  >
                    <label
                      for="tasksForMe"
                      class="text-nowrap text-primary"
                      v-html="$t('statsList.tasksWithRecordsLeftForMe')"
                    ></label>
                  </b-form-checkbox>
                  <b-form-checkbox
                    id="openTasks"
                    v-model="onlyOpenTasks"
                    class="stats-list__filters__checkbox--open-tasks mr-5"
                  >
                    <label for="openTasks" class="text-nowrap text-primary">{{ $t('statsList.openTasks') }}</label>
                  </b-form-checkbox>
                </div>
                <div class="stats-list__filters d-flex">
                  <task-sort-by-dropdown
                    :sort.sync="sortField"
                    class="stats-list__filters__sort-by"
                    @update:sort-by-cb="updateSortByCallback"
                  />
                </div>
              </div>
            </div>
            <app-waiter :loader="fetchTaskLoader" waiter-class="my-5 mx-auto d-block">
              <task-stats-card-detailed
                v-for="task in displayedTasks"
                :key="task.id"
                class="stats-list__task-card my-2 my-lg-5"
                :task-id="task.id"
                :team="teamTaskStats"
                :checker-id="me"
              />
            </app-waiter>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.stats-list__filters__sort-by {
  width: 240px;
}
</style>
