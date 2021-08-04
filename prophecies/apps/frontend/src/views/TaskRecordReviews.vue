<template>
  <div class="task-record-reviews">
    <div class="d-flex align-items-center">
      <ul class="task-record-reviews__breadcrumb list-inline flex-grow-1 mx-5">
        <li class="list-inline-item task-record-reviews__breadcrumb__item">
          <router-link :to="{ name: 'dashboard' }">
            <home-icon size="1.5x" />
          </router-link>
        </li>
        <li class="list-inline-item task-record-reviews__breadcrumb__item" v-if="task">
          {{ task.name }}
        </li>
      </ul>
      <app-header />
    </div>
    <div class="task-record-reviews__container">
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchAllLoader" waiter-class="my-5 mx-auto d-block">
          <div class="row mb-5" v-if="pagination">
            <div class="col-auto">
              <b-btn variant="outline-dark" class="border" tag="label" disabled>
                <span class="custom-control custom-checkbox">
                  <input class="custom-control-input" type="checkbox" id="select-all-input" />
                  <div class="custom-control-label" for="select-all-input">
                    Select all {{ taskRecordReviews.length }} items
                  </div>
                </span>
              </b-btn>
            </div>
            <custom-pagination
              @input="goToPage"
              class="col"
              compact
              :value="Number(page)"
              :total-rows="pagination.count"
              :per-page="10" />
            <div class="col-auto">
              <b-btn variant="outline-dark" class="border font-weight-bold" disabled>
                <filter-icon size="1x" class="mr-1" />
                Filters
              </b-btn>
            </div>
          </div>
          <div v-for="{ id } in taskRecordReviews" :key="id" class="mb-5">
            <task-record-review-card
              :task-record-review-id="id"
              :active="isTaskRecordReviewActive(id)" />
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<script>
import { get, find, uniqueId } from 'lodash'

import AppHeader from '@/components/AppHeader'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviews',
  components: {
    AppHeader,
    AppWaiter,
    TaskRecordReviewCard
  },
  props: {
    taskId: {
      type: [Number, String]
    },
    page: {
      type: [Number, String],
      default: 1
    }
  },
  data () {
    return {
      pagination: null
    }
  },
  async created () {
    await this.waitFor(this.fetchAllLoader, this.fetchAll)
  },
  computed: {
    task () {
      return Task.find(this.taskId)
    },
    tasks () {
      return Task.all()
    },
    taskRecordReviews () {
      return TaskRecordReview.query().all()
    },
    taskRecordReviewsParams () {
      return {
        'filter[task_record.task]': this.taskId,
        'page[number]': this.page
      }
    },
    fetchAllLoader () {
      return uniqueId('load-task-record-review-')
    },
    firstPendingTaskRecordReview () {
      const all = TaskRecordReview.all()
      return find(all, { status: 'PENDING' })
    }
  },
  methods: {
    fetchTask () {
      return Task.api().find(this.taskId)
    },
    fetchChoiceGroup () {
      return ChoiceGroup.api().find(this.task.choice_group_id)
    },
    async fetchTaskRecordReviews () {
      TaskRecordReview.deleteAll()
      const params = this.taskRecordReviewsParams
      const result = await TaskRecordReview.api().get('', { params })
      const pagination = get(result, 'response.data.meta.pagination', null)
      this.$set(this, 'pagination', pagination)
    },
    async goToPage (page) {
      const query = { ...this.$route_query, page }
      await this.$router.push({ path: this.$route.path, query })
      await this.waitFor(this.fetchAllLoader, this.fetchTaskRecordReviews)
    },
    isTaskRecordReviewActive (id) {
      return get(this, 'firstPendingTaskRecordReview.id') === id
    },
    async fetchAll () {
      await this.fetchTask()
      await this.fetchChoiceGroup()
      await this.fetchTaskRecordReviews()
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    }
  }
}
</script>

<style lang="scss" scoped>
  .task-record-reviews {

    &__breadcrumb {
      display: inline-flex;
      align-items: center;

      &__item.list-inline-item {
        font-size: $font-size-lg;
        padding-right: $spacer-sm;
        margin-right: 0;
        display: inline-flex;
        align-items: center;
        font-weight: 600;

        &:not(:last-of-type):after {
          content: "";
          background: center right no-repeat;
          background-size: contain;
          background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNyIgaGVpZ2h0PSIxMiIgdmlld0JveD0iMCAwIDcgMTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPHBhdGggZD0iTTEgMTAuNzIwOUw2IDUuODYwNDRMMSAxIiBzdHJva2U9IiMyMzVCNTkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
          margin-left: $spacer-sm;
          display: block;
          height: 1em;
          width: 0.5em;
        }
      }
    }
  }
</style>
