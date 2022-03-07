
<script>
import { orderBy, maxBy } from 'lodash'
import moment from 'moment'

import { TaskStatusOrder } from '@/models/Task'

import User from '@/models/User'
import ActionAggregate from '@/models/ActionAggregate'
import { formatDate } from '@/utils/date'
import LightDropdown from '@/components/LightDropdown.vue'

const ALL__OPEN_TASKS_ID = '0_all'

export default {
  components: { LightDropdown },
  name: 'UserRetrieveActivityChart',
  props: {
    lastDate: {
      type: Date
    },
    range: {
      type: Number
    },
    activityIds: {
      type: Array,
      default: () => []
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
      selectedTaskId: ALL__OPEN_TASKS_ID
    }
  },
  methods: {
    formatDate (d) {
      return formatDate(d)
    },

    async waitFor (loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns)
      this.$wait.end(loader)
    },
    activityIsSameDay (activityIndex, date) {
      return this.activities[activityIndex] && moment(this.activities[activityIndex].date).isSame(date, 'day')
    },
    activityIsBeforeDay (activityIndex, date) {
      return this.activities[activityIndex] && moment(this.activities[activityIndex].date).isBefore(date)
    }
  },
  computed: {
    user () {
      return User.find(this.username)
    },
    dropdownTasks () {
      return [
        {
          id: ALL__OPEN_TASKS_ID,
          name: this.$t('userTaskStatsCard.allOpenTasks')
        },
        ...this.tasks
      ]
    },
    tasks () {
      return Object.values(this.activities.reduce((prev, curr) => {
        prev[curr.taskId] = curr.task
        return prev
      }, {}))
    },
    activities () {
      return ActionAggregate.query()
        .whereIdIn(this.activityIds)
        .with('task')
        .get()
    },
    chartMaxValue () {
      const maxItem = maxBy(this.chartActivitiesByTaskId, 'value')
      if (maxItem) {
        return Math.round(maxItem.value * 1.2)
      }
      return 100
    },
    chartActivitiesByTaskId () {
      if (!this.activities?.length) {
        return []
      }
      const data = []
      let activityIndex = 0

      const lastDate = moment(this.lastDate).add(1, 'days')
      const range_ = (this.range + 1) * -1
      const currDate = lastDate.clone().add(range_, 'days')

      // take the first activity in the time window
      while (this.activityIsBeforeDay(activityIndex, currDate)) {
        ++activityIndex
      }
      while (currDate.add(1, 'days').diff(lastDate) < 0) {
        const size = data.push({ date: currDate.clone(), value: 0 })
        while (this.activityIsSameDay(activityIndex, currDate)) {
          const { count, taskId } = this.activities[activityIndex]
          if (this.selectedTaskId === ALL__OPEN_TASKS_ID || this.selectedTaskId === taskId) {
            data[size - 1].value += count
          }
          ++activityIndex
        }
      }
      return data
    }
  }
}
</script>

<template>
  <!--CHART -->
  <div
    class="user-retrieve-activity__chart card p-5"
  >
  <div class="d-flex">
  <div class="col-6">
    <h2 class="text-primary">Reviewed record per day</h2>
    <p class="text-muted">
      Number of classified records over the last {{range}} days on all tasks.
    </p>
  </div>
  <div class="col-6">
    <light-dropdown class="d-flex flex-row-reverse"
    :btnClassList="['btn', 'btn-lighter']"
    :items="dropdownTasks"
    :selectedId.sync="selectedTaskId"/>
</div>
  </div>
    <stacked-column-chart
      v-if="chartActivitiesByTaskId.length"
      :data="chartActivitiesByTaskId"
      :barColors="['var(--column-color)']"
      :max-value="chartMaxValue"
      no-tooltips
      hide-legend
      bar-max-width="30px"
      :x-axis-tick-format="formatDate"
      :fixedHeight="300"
      no-direct-labeling
      class="my-4"
    >
    </stacked-column-chart>
  </div>
</template>
<style lang="scss" scoped>

.user-retrieve-activity__chart {
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
</style>
