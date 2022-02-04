<script>
import { get, groupBy, remove, uniqueId } from 'lodash'
import { sortByProjectThenTask } from '@/utils/sort'

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import BookmarksPageParams from '@/components/BookmarksPageParams'
import PageHeader from '@/components/PageHeader'
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
    BookmarksPageParams,
    PageHeader
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
      FILTER_TYPES: Object.freeze(FILTER_TYPES),
      projectFilter: this.query[FILTER_TYPES.PROJECT],
      taskFilter: this.query[FILTER_TYPES.TASK],
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

      const taskRecordReviewIds = get(response, 'data.data', []).map(t => t.id)
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
      try {
        await Promise.all(uniqueChoiceGroups.promises)
      } catch (_) { }
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
      try {
        await Promise.all(uniqueTaskIds.promises)
      } catch (_) { }

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
      // keep the current project filter if no task is selected
      if (reviewsOfTask[0].task.projectId) {
        this.projectFilter = reviewsOfTask[0].task.projectId
      }
      this.taskFilter = val
      this.updateFilters()
    },
    updateFilters () {
      return this.$router.push({ name: 'user-retrieve-bookmarks', query: this.bookmarksParams })
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
    projectId: {
      get () {
        return this.query[FILTER_TYPES.PROJECT]
      },
      set (value) {
        this.setProjectFilter(value)
      }
    },
    taskId: {
      get () {
        return this.query[FILTER_TYPES.TASK]
      },
      set (value) {
        this.setTaskFilter(value)
      }
    },
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
      const bookmarks = this.taskRecordReviews.slice()
      if (this.query[FILTER_TYPES.PROJECT]) {
        remove(bookmarks, trw => trw.task.project.id !== this.query[FILTER_TYPES.PROJECT])
      }
      if (this.query[FILTER_TYPES.TASK]) {
        remove(bookmarks, trw => trw.task.id !== this.query[FILTER_TYPES.TASK])
      }
      return bookmarks.sort(sortByProjectThenTask)
    },
    bookmarksGroupedByProject () {
      return groupBy(this.filteredBookmarks, (record) => {
        return record.task.project ? record.task.project.name : ''
      })
    },
    bookmarksParams () {
      return {
        [FILTER_TYPES.PROJECT]: this.projectFilter,
        [FILTER_TYPES.TASK]: this.taskFilter
      }
    }
  }
}
</script>

<template>
  <div class="user-retrieve-bookmarks">
    <template v-if="taskRecordReviewIds.length">
      <bookmarks-page-params
        :tasks="tasks"
        :project-id.sync="projectId"
        :task-id.sync="taskId"/>
      <div v-for="(projectValue, name) in bookmarksGroupedByProject" :key="name" class="user-retrieve-bookmarks__project mt-4 mb-4 border-bottom">
        <h1 class="mb-3 mt-4 primary">{{ name }}</h1>
        <div v-for="(taskValue, taskName) in bookmarksGroupedByTask(projectValue)" :key="taskName" class="user-retrieve-bookmarks__project__task mb-4">
          <div class="d-flex flex-row mb-4 ml-4 mt-4">
            <div>
              <h2>{{ taskName }}</h2>
            </div>
          </div>
          <b-list-group-item v-for="record in taskValue" class="user-retrieve-bookmarks__project__task__record flex-column align-items-start ml-4 border-0" :key="record.id">
            <task-record-review-card
              :task-record-review-id="record.id"
              :active="true"/>
          </b-list-group-item>
        </div>
      </div>
    </template>
    <div v-else class="user-retrieve-bookmarks__no-items text-center text-secondary text-small">
      No bookmarks
    </div>
  </div>
</template>
