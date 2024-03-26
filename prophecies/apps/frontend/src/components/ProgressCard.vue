<script>
import { mean, orderBy, shuffle } from 'lodash'

import Task, { TaskStatusEnum } from '@/models/Task'
import EmptyPlaceholder from '@/components/EmptyPlaceholder'

export default {
  name: 'ProgressCard',
  components: {
    EmptyPlaceholder
  },
  filters: {
    taskProgressStyle({ colors }) {
      return `--progress-fg: ${colors[1]}`
    },
    round(value) {
      return Math.round(value)
    }
  },
  props: {
    limit: {
      type: Number,
      default: 5
    }
  },
  data() {
    return {
      team: false
    }
  },
  computed: {
    unorderedTasks() {
      // make stats on tasks with at least one record
      return Task.query()
        .where('status', (value) => value !== TaskStatusEnum.CLOSED)
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    },

    tasks() {
      const randomTasks = shuffle(this.unorderedTasks).slice(0, Math.min(this.unorderedTasks.length, this.limit))
      return orderBy(randomTasks, 'name')
    },
    nbClosedTasks() {
      // make stats on tasks with at least one record
      return Task.query()
        .where('status', (value) => value === TaskStatusEnum.CLOSED)
        .where('taskRecordsCount', (value) => value > 0)
        .get().length
    },
    meanProgress() {
      if (!this.unorderedTasks.length) {
        return 0
      }
      return mean(this.unorderedTasks.map(this.taskProgress))
    },
    progressOptions() {
      return [
        { text: this.$t('progressCard.title.yours'), value: false },
        { text: this.$t('progressCard.title.team'), value: true }
      ]
    }
  },
  methods: {
    taskProgress(task) {
      if (this.team) {
        return task.progress
      }
      return task.userProgress
    }
  }
}
</script>

<template>
  <div class="progress-card card card-body py-4 px-5 shadow-sm">
    <div class="card-flex d-flex align-items-center justify-content-start mt-3 mb-5">
      <users-icon size="1.5x" class="text-primary mr-4" />
      <b-form-radio-group
        v-model="team"
        buttons
        button-variant="outline-primary"
        :options="progressOptions"
        class="flex-grow-1"
      />
    </div>
    <template v-if="tasks.length">
      <ul class="list-unstyled progress-card__items">
        <li class="font-weight-bold progress-card__items__item progress-card__items__item--mean d-flex">
          <span class="mr-1 progress-card__items__item__value"> {{ meanProgress | round }}% </span>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="meanProgress" :max="100" class="mb-1" />
            <span class="progress-card__items__item__name">
              {{ $tc('progressCard.allOpenTasks') }} ({{ unorderedTasks.length }})
            </span>
          </div>
        </li>
        <li v-for="task in tasks" :key="task.id" class="progress-card__items__item d-flex">
          <span class="progress-card__items__item__value mr-1"> {{ taskProgress(task) | round }}% </span>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="taskProgress(task)" :style="task | taskProgressStyle" :max="100" class="mb-1" />
            <span class="progress-card__items__item__name">
              {{ task.name }}
            </span>
          </div>
        </li>
        <li v-if="nbClosedTasks" class="progress-card__items__closed-tasks d-flex">
          <span class="progress-card__items__item__value mr-1 mt-1">🎉</span>
          <div class="flex-grow-1 pt-1 pb-4 text-muted">{{ $tc('progressCard.tasksClosed', nbClosedTasks) }}</div>
        </li>
      </ul>
      <div class="progress-card__stats-link d-flex justify-content-center">
        <router-link class="btn btn-link text-secondary" :to="{ name: 'stats-list' }">
          {{ $t('progressCard.moreProgress') }}
        </router-link>
      </div>
    </template>
    <empty-placeholder v-else class="progress-card__no-items" :title="$t('progressCard.noOpenTasks')" />
  </div>
</template>

<style lang="scss" scoped>
.progress-card {
  &__items {
    &__item {
      & ::v-deep .progress-bar {
        background: var(--progress-fg, $primary) !important;
      }

      &__value {
        width: 3rem;
      }
    }
  }
}
</style>
