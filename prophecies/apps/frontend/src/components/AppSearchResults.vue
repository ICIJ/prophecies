<script>
import { escapeRegExp, find, filter, get } from 'lodash'

import Task, { TaskStatusEnum } from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import Tip from '@/models/Tip'
import ShortkeyBadge from '@/components/ShortkeyBadge'

export default {
  name: 'AppSearchResults',
  components: {
    ShortkeyBadge
  },
  props: {
    query: {
      type: String,
      default: ''
    },
    queryset: {
      type: Array,
      default: () => []
    },
    counts: {
      type: Array,
      default: () => []
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
  computed: {
    taskRecordReviewIds() {
      const type = TaskRecordReview.entity
      return filter(this.queryset, { type }).map(({ id }) => id)
    },
    tipIds() {
      const type = Tip.entity
      return filter(this.queryset, { type }).map(({ id }) => id)
    },
    tasks() {
      // retrieve tasks that are not closed and with at least one record
      return Task.query()
        .where('status', (value) => value !== TaskStatusEnum.CLOSED)
        .where('taskRecordsCount', (value) => value > 0)
        .get()
    }
  },
  watch: {
    async activeItem() {
      await this.$nextTick()
      const link = this.$el.querySelector(this.activeItemSelector)
      // Don't try to focus if there is no active link
      if (link) {
        link.focus()
      }
    }
  },
  created() {
    this.$shortkey.bind('enter', () => {
      this.$emit('shortkey:enter')
    })
  },

  methods: {
    isActive(index) {
      return index === this.activeItem
    },
    activateQueryset(querysetId) {
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
    highlight(text) {
      const regex = new RegExp('(' + escapeRegExp(this.query) + ')', 'gi')
      return text.replace(regex, '<mark class="p-0">$1</mark>')
    },
    tipQuerysetId() {
      const firstMatch = find(this.queryset, { type: Tip.entity })
      return get(firstMatch, 'querysetId', null)
    },
    taskQuerysetId(taskId) {
      const firstMatch = find(this.queryset, ({ id, type }) => {
        const sameType = type === TaskRecordReview.entity
        const sameTaskAndId = TaskRecordReview.query().where('id', id).where('taskId', taskId).exists()
        return sameType && sameTaskAndId
      })
      return get(firstMatch, 'querysetId', null)
    },
    querysetCount(querysetId) {
      const match = find(this.counts, { querysetId })
      return get(match, 'count', 0)
    },
    tipCount() {
      const querysetId = this.tipQuerysetId()
      return this.querysetCount(querysetId)
    },
    isTaskQuerysetActive(taskId) {
      return this.querysetId === this.taskQuerysetId(taskId)
    },
    isTipQuerysetActive() {
      return this.querysetId === this.tipQuerysetId()
    },
    taskRecordReviewsCount(taskId) {
      const querysetId = this.taskQuerysetId(taskId)
      return this.querysetCount(querysetId)
    },
    querysetTaskRecordReviews(taskId) {
      return TaskRecordReview.query()
        .where('taskId', taskId)
        .whereIdIn(this.taskRecordReviewIds)
        .with('taskRecord')
        .get()
    },
    querysetTips() {
      return Tip.query().whereIdIn(this.tipIds).get()
    }
  }
}
</script>

<template>
  <div class="app-search-results card card-body rounded-sm border-primary shadow-sm">
    <div class="text-right text-secondary px-4">
      <span class="align-middle">Search</span> <shortkey-badge :value="['Enter']" class="ml-2" />
    </div>
    <b-tabs
      active-nav-item-class="app-search-results__tabs__nav__active"
      class="app-search-results__tabs mt-3"
      content-class="app-search-results__tabs__content"
      end
      nav-class="app-search-results__tabs__nav"
      no-nav-style
      pills
      vertical
    >
      <b-tab
        v-for="task in tasks"
        :key="task.id"
        :active="isTaskQuerysetActive(task.id)"
        no-key-nav
        lazy
        title-item-class="app-search-results__tabs__nav__item app-search-results__tabs__nav__item--task"
        title-link-class="app-search-results__tabs__nav__item__link"
        @click="activateQueryset(taskQuerysetId(task.id))"
      >
        <template #title>
          <span class="app-search-results__tabs__nav__item__link__name" :title="task.name">{{ task.name }}</span>
          <span class="ml-auto pl-2 text-secondary">
            {{ taskRecordReviewsCount(task.id) }}
          </span>
        </template>
        <b-card-text>
          <router-link
            v-for="(review, index) in querysetTaskRecordReviews(task.id)"
            :key="review.id"
            class="app-search-results__tabs__content__link"
            :class="{ 'app-search-results__tabs__content__link--active': isActive(index) }"
            :to="{ name: 'task-record-review-retrieve', params: { taskId: task.id, taskRecordReviewId: review.id } }"
          >
            <span v-html="highlight(review.taskRecord.originalValue)"></span>
          </router-link>
        </b-card-text>
      </b-tab>
      <b-tab
        lazy
        title-item-class="app-search-results__tabs__nav__item"
        title-link-class="app-search-results__tabs__nav__item__link"
        :active="isTipQuerysetActive()"
        @click="activateQueryset(tipQuerysetId())"
      >
        <template #title>
          {{ $t('appSearchResults.tips') }}
          <span class="ml-auto pl-2 text-secondary">
            {{ tipCount() }}
          </span>
        </template>
        <b-card-text>
          <router-link
            v-for="(tip, index) in querysetTips()"
            :key="tip.id"
            class="app-search-results__tabs__content__link"
            :class="{ 'app-search-results__tabs__content__link--active': isActive(index) }"
            :to="{ name: 'tip-retrieve', params: { tipId: tip.id } }"
          >
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
    & ::v-deep &__nav {
      min-width: 200px;

      &__item {
        margin-bottom: $spacer;

        &__link {
          flex-grow: 1;
          display: block;
          text-transform: uppercase;

          &__name {
            white-space: nowrap;
            max-width: 160px;
            overflow: hidden;
            text-overflow: ellipsis;
          }
        }
      }

      &__active {
        font-weight: bolder;
        border-left: 7px solid $warning;
      }
    }

    & ::v-deep &__content {
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

        &:focus,
        &:focus:hover {
          background: $light;
          outline: none;
        }
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
}
</style>
