<script>
import { compact, get, groupBy, map, uniq, uniqueId } from 'lodash'

import { orderByProjectThenTask } from '@/utils/sort'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCardWrapper from '@/components/TaskRecordReviewCardWrapper'
import BookmarksPageParams from '@/components/BookmarksPageParams'
import EmptyPlaceholder from '@/components/EmptyPlaceholder'
import TaskStatus from '@/components/TaskStatus'
import User from '@/models/User'
import TaskRecordReview from '@/models/TaskRecordReview'
import Task from '@/models/Task'
import ChoiceGroup from '@/models/ChoiceGroup'

const FILTER_TYPES = {
  PROJECT: 'filter[project]',
  TASK: 'filter[task]'
}

export default {
  name: 'UserRetrieveBookmarks',
  components: {
    AppWaiter,
    TaskRecordReviewCardWrapper,
    BookmarksPageParams,
    EmptyPlaceholder,
    TaskStatus
  },
  props: {
    username: {
      type: String
    },
    query: {
      type: Object,
      default: () => ({
        [FILTER_TYPES.PROJECT]: null,
        [FILTER_TYPES.TASK]: null
      })
    }
  },
  data() {
    return {
      projectFilter: this.query[FILTER_TYPES.PROJECT],
      taskFilter: this.query[FILTER_TYPES.TASK],
      taskRecordReviewIds: [],
      taskIds: []
    }
  },
  computed: {
    projectId: {
      get() {
        return this.query[FILTER_TYPES.PROJECT]
      },
      set(value) {
        this.setProjectFilter(value)
      }
    },
    taskId: {
      get() {
        return this.query[FILTER_TYPES.TASK]
      },
      set(value) {
        this.setTaskFilter(value)
      }
    },
    fetchBookmarksLoader() {
      return uniqueId('load-bookmarks-')
    },
    tasks() {
      return Task.query().with('project').with('choiceGroup').whereIdIn(this.taskIds).get()
    },
    taskRecordReviews() {
      return TaskRecordReview.query()
        .with('task.project')
        .with('task')
        .with('taskRecord')
        .whereIdIn(this.taskRecordReviewIds)
        .get()
    },
    filteredBookmarks() {
      return orderByProjectThenTask(
        this.taskRecordReviews.filter(
          ({ task }) =>
            (!this.query[FILTER_TYPES.PROJECT] || task?.project?.id === this.query[FILTER_TYPES.PROJECT]) &&
            (!this.query[FILTER_TYPES.TASK] || task?.id === this.query[FILTER_TYPES.TASK])
        )
      )
    },
    bookmarksGroupedByProject() {
      return groupBy(this.filteredBookmarks, (record) => {
        return record.task.project ? record.task.project.name : ''
      })
    },
    bookmarksParams() {
      return {
        [FILTER_TYPES.PROJECT]: this.projectFilter,
        [FILTER_TYPES.TASK]: this.taskFilter
      }
    },
    user() {
      return User.find(this.username)
    }
  },
  created() {
    return this.setup()
  },
  methods: {
    async setup() {
      try {
        await this.waitFor(this.fetchBookmarksLoader, this.fetchAll)
      } catch (error) {
        const title = this.$t('userRetrieveBookmarks.unableToRetrieveTheBookmarks')
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async fetchAll() {
      await this.fetchBookmarks()
      await this.fetchTasks()
      await this.fetchChoiceGroups()
    },
    async fetchBookmarks() {
      const params = {
        'filter[checker]': this.user.id,
        'filter[task_record__bookmarked_by]': this.user.id
      }

      const { response } = await TaskRecordReview.api().get('', { params })
      const taskRecordReviewIds = map(get(response, 'data.data', []), 'id')

      this.$set(this, 'taskRecordReviewIds', taskRecordReviewIds)
    },
    fetchChoiceGroup(choiceGroupId) {
      const params = { include: 'alternative_values,choices' }
      return ChoiceGroup.api().find(choiceGroupId, { params })
    },
    fetchChoiceGroups() {
      const ids = map(this.tasks, 'choiceGroupId')
      const uniqueIds = uniq(compact(ids))

      return Promise.all(map(uniqueIds, (groupId) => this.fetchChoiceGroup(groupId)))
    },
    fetchTask(taskId) {
      const params = { include: 'project,checkers,templateSetting' }
      return Task.api().find(taskId, { params })
    },
    fetchTasks() {
      const ids = map(this.taskRecordReviews, 'taskId')
      const uniqueIds = uniq(compact(ids))
      const promises = map(uniqueIds, (taskId) => this.fetchTask(taskId))
      this.$set(this, 'taskIds', uniqueIds)
      return Promise.all(promises)
    },
    async waitFor(loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    bookmarksGroupedByTaskId(records) {
      return groupBy(records, (record) => (record.task ? record.task.id : ''))
    },
    setProjectFilter(val) {
      if (this.projectNotContainingTask(val, this.taskFilter)) {
        this.taskFilter = null
      }

      this.projectFilter = val
      this.updateFilters()
    },
    setTaskFilter(val) {
      const reviewsOfTask = TaskRecordReview.query().with('task').where('taskId', val).get()
      // keep the current project filter if no task is selected
      if (reviewsOfTask[0].task.projectId) {
        this.projectFilter = reviewsOfTask[0].task.projectId
      }
      this.taskFilter = val
      this.updateFilters()
    },
    updateFilters() {
      return this.$router.push({
        name: 'user-retrieve-bookmarks',
        query: this.bookmarksParams,
        username: this.username
      })
    },
    projectNotContainingTask(projectId, taskId) {
      const reviewsOfProject = Task.query().where('projectId', projectId).get()
      return reviewsOfProject.filter((t) => t.id === taskId).length === 0
    },
    taskNotContainingUser(taskId) {
      return TaskRecordReview.query().where('task.id', taskId)
    },
    taskName(taskId) {
      return Task.find(taskId).name
    },
    taskClosed(taskId) {
      return Task.find(taskId).closed === true
    }
  }
}
</script>

<template>
  <div class="user-retrieve-bookmarks">
    <app-waiter :loader="fetchBookmarksLoader" waiter-class="my-5 mx-auto d-block">
      <template v-if="taskRecordReviewIds.length">
        <bookmarks-page-params :tasks="tasks" :project-id.sync="projectId" :task-id.sync="taskId" />
        <div
          v-for="(projectValue, name) in bookmarksGroupedByProject"
          :key="name"
          class="user-retrieve-bookmarks__project my-4 border-bottom"
        >
          <h1 class="mb-3 mt-4 text-primary">{{ name }}</h1>
          <div
            v-for="(taskRecordReviewsBookmarked, taskIdBookmarked) in bookmarksGroupedByTaskId(projectValue)"
            :key="taskIdBookmarked"
            class="user-retrieve-bookmarks__project__task mb-4"
          >
            <div class="d-flex flex-row my-4 ml-4">
              <h2 class="text-tertiary">{{ taskName(taskIdBookmarked) }}</h2>
              <task-status
                v-if="taskIdBookmarked && taskClosed(taskIdBookmarked)"
                class="mt-0 ml-2"
                :task-id="taskIdBookmarked"
              />
            </div>
            <div
              v-for="record in taskRecordReviewsBookmarked"
              :key="record.id"
              class="user-retrieve-bookmarks__project__task__record ml-4 mb-5"
            >
              <task-record-review-card-wrapper :task-record-review-id="record.id" />
            </div>
          </div>
        </div>
      </template>
      <empty-placeholder
        v-else
        class="user-retrieve-bookmarks__empty"
        icon="BookmarkIcon"
        :title="$t('userRetrieveBookmarks.noBookmarks')"
      />
    </app-waiter>
  </div>
</template>
