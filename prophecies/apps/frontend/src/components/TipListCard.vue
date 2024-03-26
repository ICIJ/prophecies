<template>
  <div class="tip-list-card p-3">
    <app-waiter :loader="fetchFilteredTipsLoader" waiter-class="my-5 mx-auto d-block">
      <slot name="header" />
      <div :class="contentClass" class="tip-list-card__content px-5 pt-4 pb-0">
        <h2 class="tip-list-card__content__title">
          <span class="tip-list-card__content__title__task">{{ $t('tipListCard.tipsFor') }} {{ taskName }}</span>
          <b-badge class="tip-list-card__content__title__project font-weight-normal bg-transparent text-muted">{{
            projectName
          }}</b-badge>
        </h2>
        <div class="tip-list-card__content__list pb-0 pr-2">
          <empty-placeholder v-if="hasNoTips" :title="$t('tipListCard.noTips')" />
          <tip-card
            v-for="tip in tips"
            v-else
            :key="tip.id"
            :tip-id="tip.id"
            :content-class="{ tipNameMargin: 'mb-4', tipCardMargin: 'mb-5' }"
          />
        </div>
        <div class="d-flex justify-content-center">
          <button class="btn btn-primary font-weight-bold mt-3 mb-5" @click="closeTips">
            <span class="px-3">{{ $t('tipListCard.seeTipsForAllTasks') }}</span>
          </button>
        </div>
      </div>
    </app-waiter>
  </div>
</template>

<script>
import { uniqueId } from 'lodash'

import AppWaiter from '@/components/AppWaiter'
import Tip from '@/models/Tip'
import Task from '@/models/Task'
import TipCard from '@/components/TipCard'

export default {
  name: 'TipListCard',
  components: {
    AppWaiter,
    TipCard
  },
  props: {
    contentClass: {
      type: [String, Object, Array],
      default: 'w-100'
    }
  },
  data() {
    return {
      task: null
    }
  },
  computed: {
    fetchFilteredTipsLoader() {
      return uniqueId('load-filtered-tips-')
    },
    tips() {
      return Tip.query()
        .where(({ taskId }) => !taskId || taskId === this.taskId)
        .get()
    },
    hasNoTips() {
      return this.tips.length === 0
    },
    taskId() {
      return this.$route.params.taskId || null
    },
    taskName() {
      return this.task?.name
    },
    projectName() {
      return this.task?.project?.name
    }
  },
  created() {
    return this.setup()
  },
  methods: {
    async setup() {
      try {
        return this.waitFor(this.fetchFilteredTipsLoader, [this.fetchTips, this.fetchTask])
      } catch (error) {
        const title = 'Unable to retrieve tips'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor(loader, fns = []) {
      this.$wait.start(loader)
      await Promise.all(fns.map((fn) => fn()))
      this.$wait.end(loader)
    },
    fetchTips() {
      return Tip.api().get()
    },
    async fetchTask() {
      let task = Task.query().with('project').find(this.taskId)
      if (!task) {
        await Task.api().find(this.taskId)
        task = Task.query().with('project').find(this.taskId)
      }
      this.task = task
      return Promise.resolve()
    },
    closeTips() {
      this.$root.$emit('prophecies::closeTips')
    }
  }
}
</script>

<style lang="scss" scoped>
@keyframes highlightRow {
  from {
    background: #fcf3c4;
  }
  to {
    background: $primary-10;
  }
}

.tip-list-card {
  background-color: $primary-10;
  border-radius: $card-border-radius;

  &__content {
    &__title {
      color: $tertiary;
      margin-bottom: $spacer-xxl;
      position: relative;

      &__task {
        text-decoration: underline;
        text-decoration-color: $warning;
        text-decoration-thickness: 7px;
        text-underline-offset: 5px;
        line-height: 24px;

        &:after {
          content: '\00a0';
        }
      }
    }

    &__list {
      min-height: 100px;
      max-height: 65vh;
      overflow-y: scroll;
    }
  }

  /* width */
  ::-webkit-scrollbar {
    width: 6px;
  }

  /* Track */
  ::-webkit-scrollbar-track {
    background: $primary-10;
  }

  /* Handle */
  ::-webkit-scrollbar-thumb {
    background: $secondary;
  }
}
</style>
