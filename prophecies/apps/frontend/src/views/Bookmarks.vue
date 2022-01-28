<script>
import { get, groupBy, uniqueId } from 'lodash'
import { sortByProjectThenTask } from '@/utils/sort'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import BookmarksPageParams from '@/components/BookmarksPageParams'
import User from '@/models/User'
import TaskRecordReview from '@/models/TaskRecordReview'
import Task from '@/models/Task'
import ChoiceGroup from '@/models/ChoiceGroup'

const FILTER_TYPES = {
  PROJECT: 'filter[project]',
  TASK: 'filter[task]'
}

export default {
  name: 'Bookmarks',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter,
    TaskRecordReviewCard,
    BookmarksPageParams
  },
  props: {
    query: {
      type: Object,
      default: () => ({
        [FILTER_TYPES.PROJECT]: null,
        [FILTER_TYPES.TASK]: null
      })
    }
  },
  data () {
    return {
      countBy: [],
      FILTER_TYPES: FILTER_TYPES,
      projectFilter: this.query[FILTER_TYPES.PROJECT],
      taskFilter: this.query[FILTER_TYPES.TASK],
      pagination: null,
      taskRecordReviewIds: [],
      taskIds: []
    }
  },
  created () {
    return this.setup()
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchBookmarksLoader, this.fetchAll)
      } catch (error) {
        const title = 'Unable to retrieve the bookmarks'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async fetchAll () {
      await this.fetchBookmarks()
      await this.fetchTasks()
      await this.fetchChoiceGroups()
    },
    async fetchBookmarks () {
      const params = { 'filter[task_record__bookmarked_by]': User.me().id }
      const { response } = await TaskRecordReview.api().get('', { params })
      const countBy = get(response, 'data.meta.countBy', null)
      const pagination = get(response, 'data.meta.pagination', null)

      const taskRecordReviewIds = get(response, 'data.data', []).map(t => t.id)
      this.$set(this, 'countBy', countBy)
      this.$set(this, 'pagination', pagination)
      this.$set(this, 'taskRecordReviewIds', taskRecordReviewIds)
    },
    async fetchChoiceGroup (taskId) {
      const params = { include: 'alternative_values,choices' }
      return ChoiceGroup.api().find(taskId, { params })
    },
    async fetchChoiceGroups () {
      const uniqueChoiceGroups = this.tasks.reduce((acc, curr) => {
        if (!acc.choiceGroupIds[curr.choiceGroupId]) {
          acc.choiceGroupIds[curr.choiceGroupId] = true
          acc.promises.push(this.fetchChoiceGroup(curr.choiceGroupId))
        }
        return acc
      }, { choiceGroupIds: {}, promises: [] })

      await Promise.all(uniqueChoiceGroups.promises)
    },
    async fetchTask (taskId) {
      const params = { include: 'project,checkers' }
      return Task.api().find(taskId, { params })
    },
    async fetchTasks () {
      const uniqueTaskIds = this.taskRecordReviews.reduce((acc, curr) => {
        if (!acc.taskIds[curr.taskId]) {
          acc.taskIds[curr.taskId] = true
          acc.promises.push(this.fetchTask(curr.taskId))
        }
        return acc
      }, { taskIds: {}, promises: [] })

      this.$set(this, 'taskIds', Object.keys(uniqueTaskIds.taskIds))
      await Promise.all(uniqueTaskIds.promises)

      this.$set(this, 'taskRecordReviewIds', this.taskRecordReviewIds)
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    bookmarksGroupedByTask (records) {
      return groupBy(records, (record) => {
        return record.task ? record.task.name : ''
      })
    },
    setProjectFilter (val) {
      if (this.projectNotContainingTask(val, this.taskFilter)) {
        this.taskFilter = null
      }

      this.projectFilter = val
      this.updateFilters()
    },
    setTaskFilter (val) {
      const reviewsOfTask = TaskRecordReview.query().with('task').where('taskId', val).get()
      this.projectFilter = reviewsOfTask[0].task.projectId

      this.taskFilter = val
      this.updateFilters()
    },
    updateFilters () {
      return this.$router.push({ name: 'bookmarks', query: this.bookmarksParams })
    },
    projectNotContainingTask (projectId, taskId) {
      const reviewsOfProject = Task.query().where('projectId', projectId).get()
      return reviewsOfProject.filter(t => t.id === taskId).length === 0
    },
    taskNotContainingUser (taskId) {
      return TaskRecordReview.query()
        .where('task.id', taskId)
    }
  },
  computed: {
    fetchBookmarksLoader () {
      return uniqueId('load-bookmarks-')
    },
    tasks () {
      return Task
        .query()
        .with('project')
        .with('choiceGroup')
        .whereIdIn(this.taskIds)
        .get()
    },
    taskRecordReviews () {
      return TaskRecordReview
        .query()
        .with('task.project')
        .with('task')
        .with('taskRecord')
        .whereIdIn(this.taskRecordReviewIds)
        .get()
    },
    filteredBookmarks () {
      let bookmarks = this.taskRecordReviews.slice()
      if (this.query[FILTER_TYPES.PROJECT]) bookmarks = bookmarks.filter(trw => trw.task.project.id === this.query[FILTER_TYPES.PROJECT])
      if (this.query[FILTER_TYPES.TASK]) bookmarks = bookmarks.filter(trw => trw.task.id === this.query[FILTER_TYPES.TASK])
      return bookmarks.sort(sortByProjectThenTask)
    },
    bookmarksGroupedByProject () {
      return groupBy(this.filteredBookmarks, (record) => {
        return record.task.project ? record.task.project.name : ''
      })
    },
    bookmarksParams () {
      const filters = {}
      if (this.projectFilter) filters[FILTER_TYPES.PROJECT] = this.projectFilter
      if (this.taskFilter) filters[FILTER_TYPES.TASK] = this.taskFilter
      return filters
    }
  }
}
</script>

<template>
  <div class="bookmarks d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="bookmarks-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchBookmarksLoader" waiter-class="my-5 mx-auto d-block">
          <div class="d-flex flex-grow-1 align-items-center mt-3 mb-5">
            <bookmark-icon class="text-primary mr-4" />
            <h1 class="bookmarks-list__title text-primary mb-0 font-weight-bold">
              Bookmarks
            </h1>
          </div>
          <bookmarks-page-params
            :tasks="tasks"
            :project-id="query[FILTER_TYPES.PROJECT]"
            @update:projectId="setProjectFilter"
            :task-id="query[FILTER_TYPES.TASK]"
            @update:taskId="setTaskFilter"/>
          <div v-for="(projectValue, name) in bookmarksGroupedByProject" :key="name" class="mt-4 mb-4 border-bottom">
            <h1 class="mb-3 mt-4 primary">{{ name }}</h1>
            <div v-for="(taskValue, taskName) in bookmarksGroupedByTask(projectValue)" :key="taskName" class="mb-4">
              <div class="d-flex flex-row mb-4 ml-4 mt-4">
                <div>
                  <h2>{{ taskName }}</h2>
                </div>
              </div>
              <b-list-group-item v-for="record in taskValue" class="flex-column align-items-start ml-4 border-0" :key="record.id">
                <task-record-review-card
                  :task-record-review-id="record.id"
                  :active="true"/>
              </b-list-group-item>
            </div>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
</style>
