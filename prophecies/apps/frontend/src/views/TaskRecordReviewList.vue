<script>
import { compact, get, filter, find, isEqual, keys, uniqueId, values } from 'lodash'

import AppBreadcrumb from '@/components/AppBreadcrumb'
import AppHeader from '@/components/AppHeader'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewAppliedFilters from '@/components/TaskRecordReviewAppliedFilters'
import TaskRecordReviewAppliedSorting from '@/components/TaskRecordReviewAppliedSorting'
import TaskRecordReviewBulkChoiceForm from '@/components/TaskRecordReviewBulkChoiceForm'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import TaskRecordReviewFilters from '@/components/TaskRecordReviewFilters'
import TaskRecordReviewPageParams from '@/components/TaskRecordReviewPageParams'
import TaskRecordReviewTutorial from '@/components/TaskRecordReviewTutorial'
import taskRecordReviewFiltersMixin from '@/mixins/task-record-review-filters'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import User from '@/models/User'

export default {
  name: 'TaskRecordReviewList',
  mixins: [taskRecordReviewFiltersMixin],
  components: {
    AppBreadcrumb,
    AppHeader,
    AppWaiter,
    TaskRecordReviewBulkChoiceForm,
    TaskRecordReviewCard,
    TaskRecordReviewAppliedFilters,
    TaskRecordReviewAppliedSorting,
    TaskRecordReviewFilters,
    TaskRecordReviewPageParams,
    TaskRecordReviewTutorial
  },
  props: {
    taskId: {
      type: [Number, String]
    }
  },
  data () {
    return {
      pagination: null,
      selectedIds: {},
      showFilters: false,
      taskRecordReviewIds: []
    }
  },
  watch: {
    pageNumber (value) {
      if (this.pagination && this.pagination.page !== value) {
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
    },
    taskRecordReviewIds (value) {
      // Maintain a clean list of selected ids
      Object.entries(this.selectedIds).forEach(([id]) => {
        // The task record review is not present on the page anymore...
        // It needs to be deleted from the list of selected id!
        if (!value.includes(id)) {
          this.$delete(this.selectedIds, id)
        }
      })
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
        return this.taskRecordReviews.length > 0 && compact(selectedIds).length === this.taskRecordReviews.length
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
        if (isEqual({ ...this.$route.query, sort }, this.$route.query)) {
          const query = { 'page[size]': this.pageSize, ...this.routeFiltersQueryParams }
          this.$router.push({ path: this.$route.path, query }, () => {})
        }
      }
    },
    hasSorting () {
      return this.sort !== 'task_record__id'
    },
    hasFilters () {
      return !!keys(this.routeFilters).length
    },
    hasSelectedAndLockedRecords () {
      return this.selectedAndLockedIdsCount > 0
    },
    hasSelectedRecords () {
      return this.selectedIdsCount > 0
    },
    showAppliedFilters () {
      return !this.showFilters && (this.hasFilters || this.hasSorting)
    },
    isBulkSelectChoiceFormDisabled () {
      return !this.isTaskOpen || !this.hasSelectedRecords || this.$wait.is(this.bulkSelectChoiceLoader)
    },
    selectedIdsCount () {
      return this.selectedIdsList.length
    },
    selectedAndLockedIdsCount () {
      return this.selectedAndLockedIdsList.length
    },
    selectedIdsList () {
      return Object.entries(this.selectedIds).reduce((list, [id, selected]) => {
        if (selected) {
          list.push(id)
        }
        return list
      }, [])
    },
    selectedAndLockedIdsList () {
      return filter(this.selectedIdsList, id => {
        return this.isTaskRecordReviewLocked(id)
      })
    },
    selectedAndUnlockedIdsList () {
      return filter(this.selectedIdsList, id => {
        return !this.isTaskRecordReviewLocked(id)
      })
    },
    filters () {
      // Method from the mixins
      return this.getTaskFilters(this.task)
    },
    otherQueryParams () {
      return Object.entries(this.$route.query).reduce((all, [key, value]) => {
        if (!this.isFiltersParam(this.filters, { key })) {
          all[key] = value
        }
        return all
      }, {})
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
      set (routeFiltersQueryParams) {
        if (!isEqual(routeFiltersQueryParams, this.routeFiltersQueryParams)) {
          const otherQueryParams = this.otherQueryParams
          const query = { ...otherQueryParams, ...routeFiltersQueryParams }
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
    taskRecordReviews () {
      return TaskRecordReview
        .query()
        .whereIdIn(this.taskRecordReviewIds)
        .get()
    },
    taskRecordReviewsParams () {
      return {
        ...this.appliedRouteFiltersQueryParams,
        'filter[task_record__task]': this.taskId,
        'filter[checker]': User.me().id,
        'page[size]': this.pageSize,
        'page[number]': this.pageNumber,
        sort: this.sort
      }
    },
    isTaskOpen () {
      return this.task && this.task.status === 'OPEN'
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
    bulkSelectChoiceLoader () {
      return uniqueId('bulk-select-choice-')
    },
    firstPendingTaskRecordReview () {
      return TaskRecordReview.query()
              .whereIdIn(this.taskRecordReviewIds)
              .where('status', 'PENDING')
              .first()
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
        const title = 'Unable to find this resource'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    applyFilters (query) {
      return this.$router.push({ path: this.$route.path, query }, () => {})
    },
    applyPageParams ({ pageSize, sort }) {
      this.$bvModal.hide('modal-page-params')
      const query = { ...this.$route.query, 'page[size]': pageSize, sort }
      return this.$router.push({ path: this.$route.path, query }, () => {})
    },
    clearFilters () {
      this.$set(this, 'routeFilters', {})
    },
    async fetchTask () {
      const params = { include: 'project,checkers' }
      return Task.api().find(this.taskId, { params })
    },
    async fetchChoiceGroup () {
      const params = { include: 'alternative_values,choices' }
      return ChoiceGroup.api().find(this.task.choiceGroupId, { params })
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
      const element = this.$el.querySelector(selector)
      const options = { behavior: 'smooth', block: 'center' }
      if (element) {
        element.scrollIntoView(options)
      }
    },
    isTaskRecordReviewActive (id) {
      const isSelected = this.isTaskRecordReviewSelected(id)
      return !isSelected && get(this, 'firstPendingTaskRecordReview.id') === id
    },
    isTrailingTaskRecordReview (id) {
      return this.trailingTaskRecordReview.id === id
    },
    isTaskRecordReviewSelected (id) {
      return !!this.selectedIds[id]
    },
    isTaskRecordReviewLocked (id) {
      const review = TaskRecordReview.query().with('taskRecord').find(id)
      // When task record is not found, we assume the review is not locked
      return get(review, 'taskRecord.locked', false)
    },
    isTaskRecordReviewFrozen (id) {
      const isLoading = this.$wait.is(this.bulkSelectChoiceLoader)
      return isLoading && this.isTaskRecordReviewSelected(id)
    },
    selectTaskRecordReview (id, toggler) {
      this.$set(this.selectedIds, id, toggler)
    },
    async bulkSelectChoiceWithLoader (data) {
      this.$wait.start(this.bulkSelectChoiceLoader)
      await this.bulkSelectChoice(data)
      this.$wait.end(this.bulkSelectChoiceLoader)
    },
    async bulkSelectChoice (data) {
      // Avoid trying to update locked reviews
      const ids = this.selectedAndUnlockedIdsList
      // We use a dedicated method that will format the data for the JSONAPI spec
      // and return the updated object (the store shall be updated as well).
      //
      // This is done from the TaskRecordReview model, which under the hood uses
      // the Operation model for bulk operations.
      await TaskRecordReview.api().bulkSelectChoice(ids, data)
      // Operation endpoint does not return updated record,
      // so we need to fetch them ourselves
      await this.fetchTaskRecordReviews()
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

<template>
  <div class="task-record-review-list">
    <div class="d-flex align-items-center">
      <app-breadcrumb v-if="task">
        {{ task.name }}
      </app-breadcrumb>
      <app-header class="flex-grow-1" />
    </div>
    <div class="task-record-review-list__container">
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchAllLoader" waiter-class="my-5 mx-auto d-block">
          <div v-if="task && task.taskRecordsCount">
            <div class="row mb-4" v-if="pagination">
              <div class="d-none d-lg-block col-lg-3">
                <b-btn variant="outline-dark" class="border" tag="label">
                  <span class="custom-control custom-checkbox">
                    <input class="custom-control-input" v-model="selectAll" type="checkbox" id="select-all-input" />
                    <div class="task-record-review-list__container__select-all custom-control-label" for="select-all-input">
                      {{ $tc('taskRecordReviewList.selectAll',  taskRecordReviews.length ) }}
                    </div>
                  </span>
                </b-btn>
              </div>
              <div class="col-8 col-lg-6 text-lg-center" v-if="pagination">
                <div class="task-record-review-list__container__pagination">
                  <custom-pagination
                    compact
                    class="pl-0"
                    @input="goToPage"
                    :value="Number(pageNumber)"
                    :total-rows="pagination.count"
                    :per-page="Number(pageSize)" />
                  <b-button v-b-modal.modal-page-params variant="link" class="task-record-review-list__container__pagination__toggler text-secondary px-2">
                    <settings-icon size="1.5x" />
                  </b-button>
                  <b-modal id="modal-page-params" hide-header hide-footer>
                    <task-record-review-page-params
                      class="task-record-review-list__container__pagination__params"
                      :page-size="pageSize"
                      :sort="sort"
                      @submit="applyPageParams"
                      @cancel="$bvModal.hide('modal-page-params')" />
                  </b-modal>
                </div>
              </div>
              <div class="col-4 col-lg-3 d-flex">
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
                <b-btn variant="link" @click="clearFilters()" v-if="hasFilters">
                  Clear filters
                </b-btn>
              </li>
              <li class="list-inline-item">
                <task-record-review-applied-sorting
                  :sort.sync="sort"
                  class="d-inline-block" />
              </li>
              <li class="task-record-review-list__container__selected-results list-inline-item font-weight-bold" v-if="hasSelectedRecords">
                {{ $tc('taskRecordReviewList.selectedResults',  selectedIdsCount ) }} <template v-if="hasSelectedAndLockedRecords">({{ $tc('taskRecordReviewList.lockedResults',  selectedAndLockedIdsCount ) }})</template>
              </li>
            </ul>
            <b-collapse :visible="showAppliedFilters">
              <task-record-review-applied-filters
                :route-filters.sync="routeFilters"
                :task-id="taskId"
                class="d-inline-block" />
            </b-collapse>
            <b-collapse :visible="hasSelectedRecords">
              <task-record-review-bulk-choice-form
                class="pb-4 pt-3"
                :disabled="isBulkSelectChoiceFormDisabled"
                :task-id="taskId"
                activate-shortkeys
                @submit="bulkSelectChoiceWithLoader" />
            </b-collapse>
            <task-record-review-tutorial />
            <app-waiter :loader="fetchTaskRecordReviewsLoader" waiter-class="my-5 mx-auto d-block">
              <div v-for="{ id } in taskRecordReviews" :key="id" class="mb-5">
                <task-record-review-card
                  @update="scrollToActiveTaskRecordReviewCard({ id })"
                  @update:selected="selectTaskRecordReview(id, $event)"
                  :task-record-review-id="id"
                  :active="isTaskRecordReviewActive(id)"
                  :selected="isTaskRecordReviewSelected(id)"
                  :frozen="isTaskRecordReviewFrozen(id)" />
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

<style lang="scss" scoped>
  .task-record-review-list {

    &__container {

      &__pagination {
        display: inline-flex;
        align-items: center;
      }

      &__selected-results {
        text-decoration: underline;
      }

    }
  }
</style>
