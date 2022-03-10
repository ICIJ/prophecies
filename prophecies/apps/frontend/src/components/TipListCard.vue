<template>
  <div class="tip-list-card p-3">
    <app-waiter :loader="fetchFilteredTipsLoader" waiter-class="my-5 mx-auto d-block">
      <slot name="header" v-bind:taskAttributes="{ taskName, projectName }" />
      <div class="tip-list-card__content pb-0">
        <b-list-group-item v-for="tip in tips" class="tip-list-card__content__list-group-item flex-column align-items-start ml-4 border-0 mb-4" :key="tip.id">
          <tip-card :tip-id="tip.id">
            <template #tip-name>
              <h3 class="mb-4">
                {{ tip.name }}
              </h3>
            </template>
          </tip-card>
        </b-list-group-item>
      </div>
      <div class="d-flex justify-content-center">
        <button class="btn btn-primary font-weight-bold mt-3 mb-5" @click="closeTips">
          <span class="px-3">{{$t('tipListCard.seeTipsForAllTasks')}}</span>
        </button>
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
  created () {
    return this.setup()
  },
  computed: {
    fetchFilteredTipsLoader () {
      return uniqueId('load-filtered-tips-')
    },
    tips () {
      return Tip.query()
        .where(({ taskId }) => !taskId || taskId === this.taskId)
        .get()
    },
    taskId () {
      return this.$route.params.taskId || null
    },
    task () {
      return Task.query().with('project').find(this.taskId)
    },
    taskName () {
      return this.task?.name
    },
    projectName () {
      return this.task?.project?.name
    }
  },
  methods: {
    async setup () {
      try {
        this.$wait.start(this.fetchFilteredTipsLoader)
        await this.fetchTips()
        this.$wait.end(this.fetchFilteredTipsLoader)
      } catch (error) {
        const title = 'Unable to retrieve tips'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    fetchTips () {
      return Tip.api().get()
    },
    closeTips () {
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
      max-height: 700px;
      overflow-y: scroll;

      &__title {
        color: $tertiary;
        margin-bottom: $spacer-xxl;
        position: relative;
        padding-left: 2.65rem;
      }

      &__list-group-item {
        background-color: $primary-10;
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
