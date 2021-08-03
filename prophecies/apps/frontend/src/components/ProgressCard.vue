<template>
  <div class="card card-body py-4 px-5 shadow progress-card">
    <div class="card-flex align-items-center mt-3 mb-5">
      <users-icon class="text-primary mr-4" />
      <b-btn-group>
        <b-btn variant="primary" class="font-weight-bold">
          Team progress
        </b-btn>
        <b-btn variant="outline-primary">
          Your progress
        </b-btn>
      </b-btn-group>
    </div>
    <ul class="list-unstyled progress-card__items">
      <li class="font-weight-bold progress-card__items__item">
        <div class="d-flex align-items-start">
          <div class="mr-1 progress-card__items__item__value">
            {{ meanProgress }}%
          </div>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="meanProgress" :max="100" class="mb-1" />
            all open tasks
          </div>
        </div>
      </li>
      <li v-for="task in tasks" :key="task.id" class="progress-card__items__item">
        <div class="d-flex align-items-start">
          <div class="mr-1 progress-card__items__item__value">
            {{ task.progress }}%
          </div>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="task.progress" :style="task | taskProgressStyle" :max="100" class="mb-1" />
            {{ task.name }}
          </div>
        </div>
      </li>
    </ul>
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
    }
  },
  computed: {
    tasks () {
      return Task.all()
    },
    meanProgress () {
      return mean(Task.all().map(t => t.progress))
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
