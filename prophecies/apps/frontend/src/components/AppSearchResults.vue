<script>
import { escapeRegExp, filter } from 'lodash'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import Tip from '@/models/Tip'

export default {
  name: 'AppSearchResults',
  props: {
    results: {
      type: Array,
      default: () => ([])
    },
    query: {
      type: String,
      default: ''
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
      return filter(this.results, { type }).map(({ id}) => (id))
    },
    tipIds () {
      const type = TaskRecordReview.entity
      return filter(this.results, { type }).map(({ id}) => (id))
    },
    tips () {
      return Tip.query().whereIdIn(this.tipIds).get()
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
    taskRecordReviews(id) {
      return TaskRecordReview
        .query()
        .where('taskId', id)
        .whereIdIn(this.taskRecordReviewIds)
        .with('taskRecord')
        .get()
    }
  }
}
</script>

<template>
  <div class="app-search-results card card-body rounded-sm border-primary shadow-sm">
    <b-tabs
      class="app-search-results__tabs mt-3"
      nav-class="app-search-results__tabs__nav"
      content-class="app-search-results__tabs__content"
      active-nav-item-class="app-search-results__tabs__nav__active"
      no-nav-style
      pills
      vertical
      end
      v-model="activeTabIndex">
      <b-tab :title="task.name" v-for="task in tasks" :key="task.id">
        <b-card-text>
          <router-link
            class="app-search-results__tabs__content__link"
            v-for="review in taskRecordReviews(task.id)"
            :key="review.id"
            :to="{ name: 'task-record-review-retreive', params: { taskId: task.id, taskRecordReviewId: review.id } }">
            <span v-html="highlight(review.taskRecord.originalValue)"></span>
          </router-link>
        </b-card-text>
      </b-tab>
      <b-tab title="Tips" v-if="false">
        <b-card-text>
          <pre>{{ tips.length }}</pre>
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

        .nav-link {
          text-transform: uppercase;
        }

        .nav-item {
          margin-bottom: $spacer;
        }

        &__active {
          font-weight: bolder;
          border-left: 7px solid $warning;
        }
      }

      & /deep/ &__content {
        &__link {
          display: block;
          margin-bottom: $spacer;
          color: $body-color;
        }
      }
    }
  }
</style>
