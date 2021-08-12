<template>
  <div class="task-record-reviews">
    <div class="d-flex align-items-center">
      <app-breadcrumb v-if="task">
        {{ task.name }}
      </app-breadcrumb>
      <app-header class="flex-grow-1" />
    </div>
    <div class="task-record-reviews__container">
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchAllLoader" waiter-class="my-5 mx-auto d-block">
          <div class="row mb-5" v-if="pagination">
            <div class="col-auto">
              <b-btn variant="outline-dark" class="border" tag="label">
                <span class="custom-control custom-checkbox">
                  <input class="custom-control-input" v-model="selectAll" type="checkbox" id="select-all-input" />
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
              <b-btn :variant="filtersTogglerVariant" class="border font-weight-bold" @click="toggleFilters">
                <filter-icon size="1x" class="mr-1" />
                Filters
              </b-btn>
            </div>
          </div>
          <b-collapse :visible="showFilters">
            <task-record-review-filters
              :route-filters.sync="routeFilters"
              :task-id="taskId" />
          </b-collapse>
          <b-collapse :visible="!showFilters">
            <task-record-review-applied-filters
              :route-filters.sync="routeFilters"
              :task-id="taskId" />
          </b-collapse>
          <app-waiter :loader="fetchTaskRecordReviewsLoader" waiter-class="my-5 mx-auto d-block">
            <div v-for="{ id } in taskRecordReviews" :key="id" class="mb-5">
              <task-record-review-card
                @update="scrollToActiveTaskRecordReviewCard({ id })"
                @update:selected="selectTaskRecordReview(id, $event)"
                :task-record-review-id="id"
                :active="isTaskRecordReviewActive(id)"
                :selected="isTaskRecordReviewSelected(id)"  />
            </div>
            <custom-pagination
            v-if="pagination"
            @input="goToPage"
            class="mx-auto"
            compact
            :value="Number(page)"
            :total-rows="pagination.count"
            :per-page="10" />
          </app-waiter>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<script>
import { get, find, keys, uniqueId } from 'lodash'

import AppBreadcrumb from '@/components/AppBreadcrumb'
import AppHeader from '@/components/AppHeader'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import TaskRecordReviewAppliedFilters from '@/components/TaskRecordReviewAppliedFilters'
import TaskRecordReviewFilters from '@/components/TaskRecordReviewFilters'
import taskRecordReviewFiltersMixin from '@/mixins/task-record-review-filters'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import User from '@/models/User'

export default {
  name: 'TaskRecordReviews',
  mixins: [taskRecordReviewFiltersMixin],
  components: {
    AppBreadcrumb,
    AppHeader,
    AppWaiter,
    TaskRecordReviewCard,
    TaskRecordReviewAppliedFilters,
    TaskRecordReviewFilters
  },
  props: {
    taskId: {
      type: [Number, String]
    },
  },
  data () {
    return {
      pagination: null,
      selectedIds: {},
      showFilters: false
    }
  },
  watch: {
    page () {
      return this.waitFor(this.fetchAllLoader, this.fetchTaskRecordReviews)
    },
    routeFilters () {
      return this.waitFor(this.fetchTaskRecordReviewsLoader, this.fetchTaskRecordReviews)
    }
  },
  created () {
    return this.setup()
  },
  computed: {
    selectAll: {
      set (checked) {
        this.taskRecordReviews.forEach(({ id }) => {
          this.$set(this.selectedIds, id, checked)
        })
      },
      get () {
        return keys(this.selectedIds).length === this.tasks.length
      }
    },
    page () {
      return this.$route.query.page || 1
    },
    routeFiltersQueryParams () {
      return Object.entries(this.$route.query).reduce((all, [key, value]) => {
        if (key.startsWith('filter[')) {
          all[key] = value
        }
        return all
      }, {})
    },
    routeFilters: {
      get () {
        return Object.entries(this.routeFiltersQueryParams).reduce((all, [key, value]) => {
          const param = key.split('filter[').pop().split(']').shift()
          all[param] = value
          return all
        }, {})
      },
      set (query) {
        return this.$router.push({ path: this.$route.path, query }, () => {})
      }
    },
    task () {
      return Task.find(this.taskId)
    },
    tasks () {
      return Task.all()
    },
    taskRecordReviews () {
      return TaskRecordReview
        .query()
        .where('checker_id', User.me().id)
        .all()
    },
    taskRecordReviewsParams () {
      return {
        ...this.routeFiltersQueryParams,
        'filter[taskRecord.task]': this.taskId,
        'page[number]': this.page
      }
    },
    trailingTaskRecordReview () {
      return this.taskRecordReviews[this.taskRecordReviews.length - 1]
    },
    fetchAllLoader () {
      return uniqueId('load-all-task-record-review-')
    },
    fetchTaskRecordReviewsLoader () {
      return uniqueId('load-task-record-review-')
    },
    firstPendingTaskRecordReview () {
      const all = TaskRecordReview.all()
      return find(all, { status: 'PENDING' })
    },
    filtersTogglerVariant () {
      return this.showFilters ? 'primary' : 'outline-primary'
    }
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchAllLoader, this.fetchAll)
        this.$core.setPageTitle(this.task.name)
      } catch (error) {
        const title = 'Unable to found this task'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    applyFilters (query) {
      return this.$router.push({ path: this.$route.path, query }, () => {})
    },
    fetchTask () {
      return Task.api().find(this.taskId)
    },
    fetchChoiceGroup () {
      return ChoiceGroup.api().find(this.task.choiceGroup_id)
    },
    async fetchTaskRecordReviews () {
      TaskRecordReview.deleteAll()
      const params = this.taskRecordReviewsParams
      const result = await TaskRecordReview.api().get('', { params })
      const pagination = get(result, 'response.data.meta.pagination', null)
      this.$set(this, 'pagination', pagination)
    },
    async goToPage (page) {
      const query = { ...this.$route.query, page }
      await this.$router.push({ path: this.$route.path, query }, () => {})
    },
    async goToNextPage () {
      const currentPage = parseInt(this.page)
      // Don't go to a page if it doesn't exist
      if (currentPage < parseInt(this.pagination.pages)) {
        return this.goToPage(currentPage + 1)
      }
    },
    async scrollToActiveTaskRecordReviewCard ({ id }) {
      if (!this.firstPendingTaskRecordReview && this.isTrailingTaskRecordReview(id)) {
        return this.goToNextPage()
      }
      const selector = '.task-record-review-card--active'
      const options = { behavior: 'smooth', block: 'center' }
      this.$el.querySelector(selector)?.scrollIntoView(options)
    },
    isTaskRecordReviewActive (id) {
      return get(this, 'firstPendingTaskRecordReview.id') === id
    },
    isTrailingTaskRecordReview (id) {
      return this.trailingTaskRecordReview.id === id
    },
    isTaskRecordReviewSelected (id) {
      return !!this.selectedIds[id]
    },
    selectTaskRecordReview (id, toggler) {
      this.$set(this.selectedIds, id, toggler)
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
    },
    toggleFilters () {
      this.showFilters = !this.showFilters
    }
  }
}
</script>
