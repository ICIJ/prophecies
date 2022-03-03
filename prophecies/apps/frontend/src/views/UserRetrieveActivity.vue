<template>
      <div class="user-retrieve-activity container-fluid p-5">
        <div class="row">
          <div class="col-12">
            <div class="d-flex flex-wrap justify-content-between">
                <b-form-group class="user-retrieve-activity__radio d-flex  mr-5">
                  <b-form-radio-group
                  v-model="activityTab"
                  buttons
                  button-variant="outline-primary"
                  :options="tabOptions" />
                </b-form-group>

                <div  v-if="!activityTab && !isLoading" class="d-flex align-items-end ">
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
            <app-waiter  :loader="fetchTaskUserStatsLoader" waiter-class="my-5 mx-auto d-block">
              <template v-if="!activityTab">

                <task-stats-card-detailed
                  class="stats-list__task-card my-5"
                  v-for="task in tasks" :key="task.id"
                  :task-id="task.id"
                  />
              </template>

            </app-waiter>
          </div>
        </div>
      </div>
</template>

<script>
import { uniqueId, filter, orderBy } from 'lodash'
import AppWaiter from '@/components/AppWaiter'

import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task, { TaskStatusEnum, TaskStatusOrder } from '@/models/Task'

import TaskSortByDropdown from '@/components/TaskSortByDropdown.vue'

import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import User from '@/models/User'

export default {
  name: 'UserRetrieveActivity',
  components: {
    AppWaiter,
    TaskStatsCardDetailed,
    TaskSortByDropdown
  },
  props: {
    username: {
      type: String
    }
  },
  created () {
    return this.setup()
  },
  data () {
    return {
      sortField: 'status_asc',
      sortByCb: (tasks) => orderBy(tasks, function (task) {
        return TaskStatusOrder[task.status] === 1
      }),
      activityTab: false,
      taskStatusFilter: true
    }
  },
  methods: {
    getOptionKeyPath (optionName) {
      if (this.user?.isMe) {
        return ['userRetrieveActivity', optionName, 'yours'].join('.')
      }
      return ['userRetrieveActivity', optionName, 'others'].join('.')
    },
    setup () {
      return this.waitFor(this.fetchTaskUserStatsLoader, [this.fetchTaskUserStats(), this.fetchTaskUserChoiceStats()])
    },
    fetchTaskUserStats () {
      const params = { 'filter[checker]': this.user.id }
      return TaskUserStatistics.api().get('', { params })
    },
    fetchTaskUserChoiceStats () {
      const params = { include: 'checker,task.choice_group.choices', 'filter[checker]': this.user.id }
      return TaskUserChoiceStatistics.api().get('', { params })
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns)
      this.$wait.end(loader)
    }

  },
  computed: {
    fetchTaskUserStatsLoader () {
      return uniqueId('load-stats-task-user')
    },
    user () {
      return User.find(this.username)
    },
    activityOption () {
      return this.$t(this.getOptionKeyPath('title'))
    },
    statsOption () {
      return this.$t(this.getOptionKeyPath('stats'))
    },
    tabOptions () {
      return [
        { text: this.activityOption, value: true },
        { text: this.statsOption, value: false }
      ]
    },
    unorderedTasks () {
      return Task
        .query()
        .with('choiceGroup.choices')
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    tasks () {
      const sortedTasks = this.sortByCb(this.unorderedTasks)
      return this.onlyOpenTasks ? filter(sortedTasks, ['status', TaskStatusEnum.OPEN || TaskStatusEnum.LOCKED]) : sortedTasks
    },
    isLoading () {
      return this.$wait.waiting(this.fetchTaskUserStatsLoader)
    },
    onlyOpenTasks: {
      get () {
        const onlyOpenTasks = this.$route.query.only_open
        if (onlyOpenTasks === 'true') {
          return true
        }
        return false
      },
      set (value) {
        const query = { ...this.$route.query, only_open: !!value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.user-retrieve-activity__filters__sort-by
{
  width:240px;
}
</style>
