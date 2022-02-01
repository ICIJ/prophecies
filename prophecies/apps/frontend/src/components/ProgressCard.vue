<template>
  <div class="progress-card card card-body py-4 px-5 shadow-sm">
    <div class="card-flex d-flex align-items-center  justify-content-start mt-3 mb-5">
      <users-icon size="1.5x" class="text-primary mr-4" />
      <b-form-radio-group
        v-model="team"
        buttons
        button-variant="outline-primary"
        :options="progressOptions" class="flex-grow-1"/>
    </div>
    <template v-if="tasks.length">
      <ul class="list-unstyled progress-card__items">
        <li class="font-weight-bold progress-card__items__item progress-card__items__item--mean">
          <div class="d-flex align-items-start">
            <div class="mr-1 progress-card__items__item__value">
              {{ meanProgress | round }}%
            </div>
            <div class="flex-grow-1 pt-1 pb-4">
              <b-progress :value="meanProgress" :max="100" class="mb-1" />
              <span class="progress-card__items__item__name">
                all open tasks
              </span>
            </div>
          </div>
        </li>
        <li v-for="task in tasks" :key="task.id" class="progress-card__items__item">
          <div class="d-flex align-items-start">
            <div class="mr-1 progress-card__items__item__value">
              {{ taskProgress(task) | round }}%
            </div>
            <div class="flex-grow-1 pt-1 pb-4">
              <b-progress :value="taskProgress(task)" :style="task | taskProgressStyle" :max="100" class="mb-1" />
              <span class="progress-card__items__item__name">
                {{ task.name }}
              </span>
            </div>
          </div>
        </li>
      </ul>
      <div class="progress-card__stats-link d-flex justify-content-center">
        <router-link class="btn btn-link text-secondary" :to="{ name: 'stats-list' }">
          {{ $t("progressCard.moreProgress") }}
        </router-link>
      </div>
    </template>
    <div v-else class="progress-card__no-items text-center text-secondary text-small">
      No open tasks
    </div>
  </div>
</template>

<script>
import { mean } from 'lodash'
import Task from '@/models/Task'

export default {
  name: 'ProgressCard',
  filters: {
    taskProgressStyle ({ colors }) {
      return `--progress-fg: ${colors[1]}`
    },
    round (value) {
      return Math.round(value)
    }
  },
  data () {
    return {
      team: true
    }
  },
  methods: {
    taskProgress (task) {
      if (this.team) {
        return task.progress
      }
      return task.userProgress
    }
  },
  computed: {
    tasks () {
      // make stats on tasks with at least one record
      return Task.query().where('status', (value) => value !== 'CLOSED').where('taskRecordsCount', (value) => value > 0).get()
    },
    meanProgress () {
      if (!this.tasks.length) {
        return 0
      }
      return mean(this.tasks.map(this.taskProgress))
    },
    progressOptions () {
      return [
        { text: 'Team progress', value: true },
        { text: 'Your progress', value: false }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
  .progress-card {

    &__items {

      &__item {

        & /deep/ .progress-bar {
          background: var(--progress-fg, $primary) !important;
        }

        &__value {
          width: 3rem;
        }
      }
    }
  }
</style>
