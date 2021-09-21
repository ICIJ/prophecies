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
    },
    activeItem: {
      type: Number,
      default: -1
    },
    activeItemSelector: {
      type: String,
      default: '.app-search-results__tabs__content__link--active'
    },
    /**
     * Id of the active queryset.
     */
    activeQuerysetId: {
      type: String
    }
  },
  watch: {
    async activeItem () {
      await this.$nextTick()
      const link = this.$el.querySelector(this.activeItemSelector)
      // Don't try to focus if there is no active link
      if (link) {
        link.focus()
      }
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
    isActive (index) {
      return index === this.activeItem
    },
    activateQueryset (querysetId) {
      /**
       * Update `active-queryset-id` model value
       * @event update:active-queryset-id
       */
      this.$emit('update:active-queryset-id', querysetId)
      /**
       * Update `active` model value
       * @event update:active-item
       */
      this.$emit('update:active-item', -1)
    },
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
    isTaskQuerysetActive (taskId) {
      return this.querysetId === this.taskQuerysetId(taskId)
    },
    isTipQuerysetActive (taskId) {
      return this.querysetId === this.tipQuerysetId()
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
      active-nav-item-class="app-search-results__tabs__nav__active"
      class="app-search-results__tabs mt-3"
      content-class="app-search-results__tabs__content"
      end
      nav-class="app-search-results__tabs__nav"
      no-nav-style
      pills
      vertical>
      <b-tab
        :active="isTaskQuerysetActive(task.id)"
        :key="task.id"
        @click="activateQueryset(taskQuerysetId(task.id))"
        lazy
        title-item-class="app-search-results__tabs__nav__item app-search-results__tabs__nav__item--task"
        title-link-class="app-search-results__tabs__nav__item__link"
        v-for="task in tasks">
        <template #title>
          {{ task.name }}
          <span class="ml-auto pl-1 text-secondary">
            {{ taskRecordReviewsCount(task.id) }}
          </span>
        </template>
        <b-card-text>
          <router-link
            class="app-search-results__tabs__content__link"
            v-for="(review, index) in querysetTaskRecordReviews(task.id)"
            :class="{ 'app-search-results__tabs__content__link--active': isActive(index) }"
            :key="review.id"
            :to="{ name: 'task-record-review-retrieve', params: { taskId: task.id, taskRecordReviewId: review.id } }">
            <span v-html="highlight(review.taskRecord.originalValue)"></span>
          </router-link>
        </b-card-text>
      </b-tab>
      <b-tab
        lazy
        title-item-class="app-search-results__tabs__nav__item"
        title-link-class="app-search-results__tabs__nav__item__link"
        :active="isTipQuerysetActive()"
        @click="activateQueryset(tipQuerysetId())">
        <template #title>
          Tips
          <span class="ml-auto pl-1 text-secondary">
            {{ tipCount() }}
          </span>
        </template>
        <b-card-text>
          <router-link
            class="app-search-results__tabs__content__link"
            :class="{ 'app-search-results__tabs__content__link--active': isActive(index) }"
            v-for="(tip, index) in querysetTips()"
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
          border-radius: $border-radius-sm;
          color: $body-color;

          &:hover {
            background: $lighter;
          }

          &:focus, &:focus:hover {
            background: $light;
            outline: none;
          }
        }
      }
    }
  }
</style>
