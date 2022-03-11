<script>
import { uniqueId, filter, orderBy } from 'lodash'
import moment from 'moment'

import AppWaiter from '@/components/AppWaiter'

import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task, { TaskStatusEnum, TaskStatusOrder } from '@/models/Task'

import TaskSortByDropdown from '@/components/TaskSortByDropdown.vue'
import UserRetrieveActivityChart from '@/components/UserRetrieveActivityChart.vue'

import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import User from '@/models/User'
import ActionAggregate from '@/models/ActionAggregate'
import { formatDate } from '@/utils/date'

export default {
  name: 'UserRetrieveActivity',
  components: {
    AppWaiter,
    TaskStatsCardDetailed,
    TaskSortByDropdown,
    UserRetrieveActivityChart
  },
  props: {
    username: {
      type: String
    }
  },
  watch: {
    activityTab: {
      immediate: true,
      handler (activityTab) {
        if (activityTab) {
          this.waitFor(this.fetchActivityLoader, [
            this.fetchActivityIds(this.user.id)
          ])
        } else {
          this.waitFor(this.fetchActivityLoader, [
            this.fetchTaskUserStats(),
            this.fetchTaskUserChoiceStats()
          ])
        }
      }
    }
  },
  data () {
    return {
      sortField: 'status_asc',
      sortByCb: (tasks) =>
        orderBy(tasks, function (task) {
          return TaskStatusOrder[task.status] === 1
        }),
      taskStatusFilter: true,
      lastDate: new Date(),
      range: 15
    }
  },
  methods: {
    formatDate (d) {
      return formatDate(d)
    },
    getOptionKeyPath (optionName) {
      if (this.user?.isMe) {
        return ['userRetrieveActivity', optionName, 'yours'].join('.')
      }
      return ['userRetrieveActivity', optionName, 'others'].join('.')
    },
    fetchActivityIds (userId) {
      const params = {
        date_after: this.lastDateParam,
        'filter[user]': userId
      }
      return ActionAggregate.api().get('', { params })
    },
    fetchTaskUserStats () {
      const params = { 'filter[checker]': this.user.id }
      return TaskUserStatistics.api().get('', { params })
    },
    fetchTaskUserChoiceStats () {
      const params = {
        include: 'checker,task.choice_group.choices',
        'filter[checker]': this.user.id
      }
      return TaskUserChoiceStatistics.api().get('', { params })
    },
    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns)
      this.$wait.end(loader)
    },
    updateSortByCallback (cb) {
      this.sortByCb = cb
    }
  },
  computed: {
    fetchTaskUserStatsLoader () {
      return uniqueId('load-stats-task-user')
    },
    fetchActivityLoader () {
      return uniqueId('load-activity-chart-')
    },
    isLoadingStats () {
      return this.$wait.waiting(this.fetchTaskUserStatsLoader)
    },
    lastDateParam () {
      const range_ = this.range * -1
      return moment(this.lastDate).clone().add(range_, 'days').format('YYYY-MM-DD').toString()
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
    activities () {
      return ActionAggregate.query()
        .where('userId', this.user.id)
        .where('verb', 'reviewed')
        .get()
    },
    activityIds () {
      return this.activities.map(a => a.id)
    },
    unorderedTasks () {
      return Task.query()
        .with('choiceGroup.choices')
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },
    tasks () {
      const sortedTasks = this.sortByCb(this.unorderedTasks)
      if (this.onlyOpenTasks) {
        return filter(sortedTasks, [
          'status',
          TaskStatusEnum.OPEN || TaskStatusEnum.LOCKED
        ])
      }
      return sortedTasks
    },
    activityTab: {
      get () {
        return this.$route.query.view !== 'stats'
      },
      set (value) {
        const query = { view: value ? 'chart' : 'stats' }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    },
    onlyOpenTasks: {
      get () {
        return this.$route.query.only_open === 'true'
      },
      set (value) {
        const query = { ...this.$route.query, only_open: !!value }
        this.$router.push({ path: this.$route.path, query }, null)
      }
    }
  }
}
</script>

<template>
  <div class="user-retrieve-activity container-fluid p-5">
    <div class="row">
      <div class="col-12">
        <div
          class="
            user-retrieve-activity__header
            d-flex
            flex-wrap
            justify-content-between
          "
        >
          <b-form-group class="d-flex mr-5">
            <b-form-radio-group
              v-model="activityTab"
              buttons
              button-variant="outline-primary"
              :options="tabOptions"
              class="user-retrieve-activity__header__tabs"
            />
          </b-form-group>
          <!--STATS FILTER -->
          <div
            v-if="!activityTab && !isLoadingStats"
            class="
              user-retrieve-activity__stats__filters
              d-flex
              align-items-end
            "
          >
            <b-form-checkbox
              class="
                user-retrieve-activity__stats__filters--open-tasks-checkbox
                mb-4
                mr-5
                pb-1
              "
              v-model="onlyOpenTasks"
            >
              <span class="text-nowrap text-primary">{{
                $t("statsList.showOnlyOpenTasks")
              }}</span>
            </b-form-checkbox>
            <task-sort-by-dropdown
              :sort.sync="sortField"
              @update:sort-by-cb="updateSortByCallback"
              class="mb-3 user-retrieve-activity__stats__filters--sort-by"
            />
          </div>
          <!---------->
        </div>
        <!--CHART -->
        <app-waiter
          v-if="activityTab"
          :loader="fetchActivityLoader"
          waiter-class="my-5 mx-auto d-block "
        >
        <user-retrieve-activity-chart
          :activity-ids="activityIds"
          :last-date="lastDate"
          :range="range"
          />
        </app-waiter>
        <!--STATS -->
        <app-waiter
          v-else
          :loader="fetchTaskUserStatsLoader"
          waiter-class="my-5 mx-auto d-block "
          class="user-retrieve-activity__stats"
        >
          <task-stats-card-detailed
            class="user-retrieve-activity__stats__task-card my-5"
            v-for="task in tasks"
            :key="task.id"
            :task-id="task.id"
            :checker-id="user.id"
          />
        </app-waiter>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>

.user-retrieve-activity {
  &__stats {

    &__filters--sort-by {
      width: 240px;
    }
  }

}
</style>
