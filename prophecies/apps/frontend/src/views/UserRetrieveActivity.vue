
<script>
import { uniqueId, filter, orderBy, maxBy } from 'lodash'
import moment from 'moment'

import AppWaiter from '@/components/AppWaiter'

import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task, { TaskStatusEnum, TaskStatusOrder } from '@/models/Task'

import TaskSortByDropdown from '@/components/TaskSortByDropdown.vue'

import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import User from '@/models/User'
import ActionAggregate from '@/models/ActionAggregate'
import { fetchActivityIds } from '@/utils/history'
import { formatDate } from '@/utils/date'

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
  watch: {
    activityTab: {
      immediate: true,
      handler (activityTab) {
        if (activityTab) {
          this.waitFor(this.fetchActivityLoader, [
            fetchActivityIds(this.user.id)
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
      activityTab: true,
      taskStatusFilter: true,
      dayRange: 15
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
    },
    isSameDate (activityIndex, date) {
      return this.activities[activityIndex] && moment(this.activities[activityIndex].date).isSame(date, 'day')
    }

  },
  computed: {
    fetchTaskUserStatsLoader () {
      return uniqueId('load-stats-task-user')
    },
    fetchActivityLoader () {
      return uniqueId('load-activity-chart-')
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
    chartMaxValue () {
      const maxItem = maxBy(this.chartActivities, 'value')
      if (maxItem) {
        return Math.round(maxItem.value * 1.2)
      }
      return 100
    },
    chartActivities () {
      if (!this.activities?.length) {
        return []
      }
      const data = []

      const lastDate = moment().add(1, 'days')
      const currDate = lastDate.clone().add(-16, 'days')

      let activityIndex = 0
      // take the first activity in the time window
      while (this.activities[activityIndex] && moment(this.activities[activityIndex].date).isBefore(currDate)) {
        activityIndex++
      }
      while (currDate.add(1, 'days').diff(lastDate) < 0) {
        if (!this.isSameDate(activityIndex, currDate)) {
          data.push({ date: currDate.clone(), value: 0 })
        } else {
          let index
          do {
            const { count } = this.activities[activityIndex]
            if (index) {
              data[index].value += count
            } else {
              data.push({ date: currDate.clone(), value: count })
              index = data.length - 1
            }
            activityIndex++
          } while (this.isSameDate(activityIndex, currDate))
        }
      }

      return data

      // return this.activities?.map((a) => ({ value: a.count, date: a.date }))
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
            v-if="!activityTab && !isLoading"
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
          class="user-retrieve-activity__chart card p-5"
        >
          <h2 class="text-primary">Reviewed record per day</h2>
          <p class="text-muted">
            Number of classified records over the last 15 days on all tasks.
          </p>
          <stacked-column-chart
            v-if="chartActivities.length"
            :data="chartActivities"
            :barColors="['var(--column-color)']"
            :max-value="chartMaxValue"
            no-tooltips

            bar-max-width="30px"
            :x-axis-tick-format="formatDate"
            :fixedHeight="300"
            no-direct-labeling
            class="my-4"
          >
          </stacked-column-chart>

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

  &__chart {
    background: $primary-10;
    --column-color: #{$primary};

    & /deep/ .stacked-column-chart {

      &__groups__item {

          &__bars {
            border-bottom: solid 2px $primary_70;

            &__item__value {
              transform: translateY(-100%);
              color: $primary;
              font-weight: bold;
              display:block !important;
            }

          }

          &__label {
            color: $primary;
          }

          &:not(:hover) {
            .stacked-column-chart__groups__item__bars__item{
                filter: grayscale(100%) brightness(2);
              }
            &:not(:nth-child(7n+1)) .stacked-column-chart__groups__item__label
             {
                  visibility: hidden;
                }

          }

      }

      & svg {
        width: 100%;
        .tick {
          text{
            color:$primary;
          }
          line{
            display: none;
          }
        }
      }
    }
  }
}
</style>
