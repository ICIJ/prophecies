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
          <div v-if="task && task.taskRecordsCount">
            <div class="row mb-4" v-if="pagination">
              <div class="col">
                <b-btn variant="outline-dark" class="border" tag="label">
                  <span class="custom-control custom-checkbox">
                    <input class="custom-control-input" v-model="selectAll" type="checkbox" id="select-all-input" />
                    <div class="custom-control-label" for="select-all-input">
                      Select all {{ taskRecordReviews.length }} items
                    </div>
                  </span>
                </b-btn>
              </div>
              <div class="col-6 text-center" v-if="pagination">
                <div class="task-record-reviews__container__pagination">
                  <custom-pagination
                    compact
                    @input="goToPage"
                    :value="Number(pageNumber)"
                    :total-rows="pagination.count"
                    :per-page="Number(pageSize)" />
                  <settings-icon
                    @click="togglePageParams"
                    class="mr-3 text-secondary task-record-reviews__container__pagination__toggler"
                    size="1.5x" />
                  <task-record-review-page-params
                    v-if="showPageParams"
                    class="task-record-reviews__container__pagination__params"
                    :page-size.sync="pageSize"
                    :sort.sync="sort" />
                </div>
              </div>
              <div class="col d-flex">
                <div class="ml-auto">
                  <b-btn :variant="filtersTogglerVariant" class="border font-weight-bold" @click="toggleFilters">
                    <filter-icon size="1x" class="mr-1" />
                    Filters
                  </b-btn>
                </div>
              </div>
            </div>
            <b-collapse :visible="showFilters">
              <task-record-review-filters
                :route-filters.sync="routeFilters"
                :task-id="taskId" />
            </b-collapse>
            <ul class="list-inline d-flex align-items-center" v-if="pagination">
              <li class="list-inline-item font-weight-bold">
                {{ pagination.count }} results
              </li>
              <li class="list-inline-item">
                <b-btn variant="link" @click="clearFilters()" :disabled="!hasFilters">
                  Clear filters
                </b-btn>
              </li>
            </ul>
            <b-collapse :visible="!showFilters && hasFilters">
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
                compact
                v-if="pagination"
                @input="goToPage"
                :value="Number(pageNumber)"
                :total-rows="pagination.count"
                :per-page="Number(pageSize)" />
            </app-waiter>
          </div>
          <div v-else class="text-center text-muted text-small mx-auto">
            No records assigned yet.
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<script>
import { compact, get, find, isEqual, keys, uniqueId, values } from 'lodash'

import AppBreadcrumb from '@/components/AppBreadcrumb'
import AppHeader from '@/components/AppHeader'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import TaskRecordReviewAppliedFilters from '@/components/TaskRecordReviewAppliedFilters'
import TaskRecordReviewFilters from '@/components/TaskRecordReviewFilters'
import TaskRecordReviewPageParams from '@/components/TaskRecordReviewPageParams'
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
    TaskRecordReviewFilters,
    TaskRecordReviewPageParams
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
      showFilters: false,
      showPageParams: false,
      taskRecordReviewIds: []
    }
  },
  watch: {
    pageNumber (value) {
      if (this.pagination?.page !== value) {
        return this.waitFor(this.fetchTaskRecordReviewsLoader, this.fetchTaskRecordReviews)
      }
    },
    pageSize () {
      return this.waitFor(this.fetchTaskRecordReviewsLoader, this.fetchTaskRecordReviews)
    },
    sort () {
      return this.waitFor(this.fetchTaskRecordReviewsLoader, this.fetchTaskRecordReviews)
    },
    routeFilters (value, previousValue) {
      if (!isEqual(value, previousValue)) {
        return this.waitFor(this.fetchTaskRecordReviewsLoader, this.fetchTaskRecordReviews)
      }
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
        const selectedIds = values(this.selectedIds)
        return compact(selectedIds).length === this.taskRecordReviews.length
      }
    },
    pageNumber () {
      return Number(this.$route.query['page[number]']) || 1
    },
    pageSize: {
      get () {
        return String(this.$route.query['page[size]'] || '10')
      },
      set (pageSize) {
        const query = { ...this.$route.query, 'page[size]': pageSize }
        this.$router.push({ path: this.$route.path, query }, () => {})
      }
    },
    sort: {
      get () {
        return this.$route.query.sort || 'task_record__id'
      },
      set (sort) {
        const query = { ...this.$route.query, sort }
        this.$router.push({ path: this.$route.path, query }, () => {})
      }
    },
    hasFilters () {
      return !!keys(this.routeFilters).length
    },
    filters () {
      // Method from the mixins
      return this.getTaskFilters(this.task)
    },
    routeFiltersQueryParams () {
      return Object.entries(this.$route.query).reduce((all, [key, value]) => {
        if (this.isFiltersParam(this.filters, { key })) {
          all[key] = value
        }
        return all
      }, {})
    },
    routeFilters: {
      get () {
        return Object.entries(this.$route.query).reduce((all, [key, value]) => {
          if (this.isFiltersParam(this.filters, { key })) {
            all[key] = value
          }
          return all
        }, {})
      },
      set (query) {
        if (!isEqual(query, this.routeFiltersQueryParams)) {
          return this.$router.push({ path: this.$route.path, query }, () => {})
        }
      }
    },
    appliedRouteFiltersQueryParams () {
      return this.mapRouteFiltersToAppliedQueryParams(this.routeFilters, this.task)
    },
    task () {
      return Task
        .query()
        .with('checkers')
        .with('choiceGroup')
        .with('choiceGroup.alternativeValues')
        .with('choiceGroup.choices')
        .find(this.taskId)
    },
    tasks () {
      return Task.all()
    },
    taskRecordReviews () {
      return TaskRecordReview
        .query()
        .whereIdIn(this.taskRecordReviewIds)
        .get()
    },
    taskRecordReviewsParams () {
      return {
        ...this.appliedRouteFiltersQueryParams,
        'filter[taskRecord.task]': this.taskId,
        'page[number]': this.pageNumber,
        'page[size]': this.pageSize,
        'sort': this.sort
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
        const title = 'Unable to find this task'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    applyFilters (query) {
      return this.$router.push({ path: this.$route.path, query }, () => {})
    },
    clearFilters () {
      this.$set(this, 'routeFilters', {})
    },
    fetchTask () {
      return Task.api().find(this.taskId)
    },
    fetchChoiceGroup () {
      return ChoiceGroup.api().find(this.task.choiceGroupId)
    },
    async fetchTaskRecordReviews () {
      const params = this.taskRecordReviewsParams
      const { response } = await TaskRecordReview.api().get('', { params })
      const pagination = get(response, 'data.meta.pagination', null)
      const taskRecordReviewIds = get(response, 'data.data', []).map(t => t.id)
      this.$set(this, 'pagination', pagination)
      this.$set(this, 'taskRecordReviewIds', taskRecordReviewIds)
    },
    async goToPage (pageNumber) {
      const query = { ...this.$route.query, 'page[number]': pageNumber }
      await this.$router.push({ path: this.$route.path, query }, () => {})
    },
    async goToNextPage () {
      const currentPage = parseInt(this.pageNumber)
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
    },
    togglePageParams () {
      this.showPageParams = !this.showPageParams
    }
  }
}
</script>

<style lang="scss" scoped>
  .task-record-reviews {
    &__container {

      &__pagination {
        display: inline-flex;
        align-items: center;
        position: relative;

        &__toggler {
          cursor: pointer;
        }

        &__params {
          z-index: $zindex-dropdown - 10;
          position: absolute;
          left: 100%;
          top: 50%;
          transform: translateY(-50%);
        }
      }
    }
  }
</style>
