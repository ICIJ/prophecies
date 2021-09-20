<script>
import { escapeRegExp, first, find, filter, get } from 'lodash'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import Tip from '@/models/Tip'

export default {
  name: 'AppSearchResults',
  props: {
    query: {
      type: String,
      default: ''
    },
    queryset: {
      type: Array,
      default: () => ([])
    },
    counts: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      activeTabIndex: 0
    }
  },
  computed: {
    taskRecordReviewIds () {
      const type = TaskRecordReview.entity
      return filter(this.queryset, { type }).map(({ id }) => id)
    },
    tipIds () {
      const type = Tip.entity
      return filter(this.queryset, { type }).map(({ id }) => id)
    },
    tasks () {
      return Task.all()
    }
  },
  methods: {
    highlight (text) {
      const regex = new RegExp("(" + escapeRegExp(this.query) + ")", "gi")
      return text.replace(regex, '<mark class="p-0">$1</mark>')
    },
    tipQuerysetId () {
      const firstMatch = find(this.queryset, { type: Tip.entity })
      return get(firstMatch, 'querysetId', null)
    },
    taskQuerysetId (taskId) {
      const firstMatch = find(this.queryset, ({ id, type }) => {
        const sameType = type === TaskRecordReview.entity
        const sameTaskAndId = TaskRecordReview.query()
          .where('id', id)
          .where('taskId', taskId)
          .exists()
        return sameType && sameTaskAndId
      })
      return get(firstMatch, 'querysetId', null)
    },
    querysetCount (querysetId) {
      const match = find(this.counts, { querysetId })
      return get(match, 'count', 0)
    },
    tipCount () {
      const querysetId = this.tipQuerysetId()
      return this.querysetCount(querysetId)
    },
    taskRecordReviewsCount (taskId) {
      const querysetId = this.taskQuerysetId(taskId)
      return this.querysetCount(querysetId)
    },
    querysetTaskRecordReviews(taskId) {
      return TaskRecordReview
        .query()
        .where('taskId', taskId)
        .whereIdIn(this.taskRecordReviewIds)
        .with('taskRecord')
        .get()
    },
    querysetTips () {
      return Tip.query().whereIdIn(this.tipIds).get()
    }
  }
}
</script>

<template>
  <div class="app-search-results card card-body rounded-sm border-primary shadow-sm">
    <b-tabs
      class="app-search-results__tabs mt-3"
      content-class="app-search-results__tabs__content"
      nav-class="app-search-results__tabs__nav"
      active-nav-item-class="app-search-results__tabs__nav__active"
      no-nav-style
      pills
      vertical
      end
      v-model="activeTabIndex">
      <b-tab
        title-item-class="app-search-results__tabs__nav__item app-search-results__tabs__nav__item--task"
        title-link-class="app-search-results__tabs__nav__item__link"
        v-for="task in tasks"
        :key="task.id">
        <template #title>
          {{ task.name }}
          <span class="ml-auto text-secondary">
            {{ taskRecordReviewsCount(task.id) }}
          </span>
        </template>
        <b-card-text>
          <router-link
            class="app-search-results__tabs__content__link"
            v-for="review in querysetTaskRecordReviews(task.id)"
            :key="review.id"
            :to="{ name: 'task-record-review-retreive', params: { taskId: task.id, taskRecordReviewId: review.id } }">
            <span v-html="highlight(review.taskRecord.originalValue)"></span>
          </router-link>
        </b-card-text>
      </b-tab>
      <b-tab
        title-item-class="app-search-results__tabs__nav__item"
        title-link-class="app-search-results__tabs__nav__item__link">
        <template #title>
          Tips
          <span class="ml-auto text-secondary">
            {{ tipCount() }}
          </span>
        </template>
        <b-card-text>
          <router-link
            class="app-search-results__tabs__content__link"
            v-for="tip in querysetTips()"
            :key="tip.id"
            :to="{ name: 'tip-retreive', params: { tipId: tip.id } }">
            <span v-html="highlight(tip.name)"></span>
          </router-link>
        </b-card-text>
      </b-tab>
    </b-tabs>
  </div>
</template>

<style lang="scss" scoped>
  .app-search-results {
    &__tabs {
      & /deep/ &__nav {
        min-width: 200px;

        &__item {
          margin-bottom: $spacer;

          &__link {
            flex-grow: 1;
            display: block;
            text-transform: uppercase;
          }
        }

        &__active {
          font-weight: bolder;
          border-left: 7px solid $warning;
        }
      }

      & /deep/ &__content {
        max-height: 70vh;
        overflow: auto;

        &__link {
          padding: $spacer-sm;
          display: block;
          margin-bottom: $spacer;
          color: $body-color;

          &:hover {
            background: $light;
            border-radius: $border-radius-sm;
          }
        }
      }
    }
  }
</style>
