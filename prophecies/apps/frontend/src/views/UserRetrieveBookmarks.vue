<script>
import { get, groupBy, remove, uniqueId } from 'lodash'
import { orderByProjectThenTask } from '@/utils/sort'
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
  name: 'UserRetrieveBookmarks',
  components: {
    AppWaiter,
    TaskRecordReviewCard,
    BookmarksPageParams
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
  data () {
    return {
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
        const title = this.$t(
          'userRetrieveBookmarks.unableToRetrieveTheBookmarks'
        )
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async fetchAll () {
      await this.fetchBookmarks()
      await this.fetchTasks()
      await this.fetchChoiceGroups()
    },
    async fetchBookmarks () {
      const params = {
        'filter[checker]': this.user.id,
        'filter[task_record__bookmarked_by]': this.user.id
      }
      const { response } = await TaskRecordReview.api().get('', { params })

      const taskRecordReviewIds = get(response, 'data.data', []).map(
        (t) => t.id
      )
      this.$set(this, 'taskRecordReviewIds', taskRecordReviewIds)
    },
    fetchChoiceGroup (taskId) {
      const params = { include: 'alternative_values,choices' }
      return ChoiceGroup.api().find(taskId, { params })
    },
    fetchChoiceGroups () {
      const uniqueChoiceGroups = this.tasks?.reduce(
        (acc, curr) => {
          if (!acc.choiceGroupIds[curr.choiceGroupId]) {
            acc.choiceGroupIds[curr.choiceGroupId] = true
            acc.promises.push(this.fetchChoiceGroup(curr.choiceGroupId))
          }
          return acc
        },
        { choiceGroupIds: {}, promises: [] }
      )

      return Promise.all(uniqueChoiceGroups.promises)
    },
    fetchTask (taskId) {
      const params = { include: 'project,checkers' }
      return Task.api().find(taskId, { params })
    },
    fetchTasks () {
      const uniqueTaskIds = this.taskRecordReviews.reduce(
        (acc, curr) => {
          if (!acc.taskIds[curr.taskId]) {
            acc.taskIds[curr.taskId] = true
            acc.promises.push(this.fetchTask(curr.taskId))
          }
          return acc
        },
        { taskIds: {}, promises: [] }
      )

      this.$set(this, 'taskIds', Object.keys(uniqueTaskIds.taskIds))
      return Promise.all(uniqueTaskIds.promises)
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
      const reviewsOfTask = TaskRecordReview.query()
        .with('task')
        .where('taskId', val)
        .get()
      // keep the current project filter if no task is selected
      if (reviewsOfTask[0].task.projectId) {
        this.projectFilter = reviewsOfTask[0].task.projectId
      }
      this.taskFilter = val
      this.updateFilters()
    },
    updateFilters () {
      return this.$router.push({
        name: 'user-retrieve-bookmarks',
        query: this.bookmarksParams,
        username: this.username
      })
    },
    projectNotContainingTask (projectId, taskId) {
      const reviewsOfProject = Task.query().where('projectId', projectId).get()
      return reviewsOfProject.filter((t) => t.id === taskId).length === 0
    },
    taskNotContainingUser (taskId) {
      return TaskRecordReview.query().where('task.id', taskId)
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
      return Task.query()
        .with('project')
        .with('choiceGroup')
        .whereIdIn(this.taskIds)
        .get()
    },
    taskRecordReviews () {
      return TaskRecordReview.query()
        .with('task.project')
        .with('task')
        .with('taskRecord')
        .whereIdIn(this.taskRecordReviewIds)
        .get()
    },
    filteredBookmarks () {
      const bookmarks = this.taskRecordReviews.slice()
      if (this.query[FILTER_TYPES.PROJECT]) {
        remove(
          bookmarks,
          (trw) => trw.task.project.id !== this.query[FILTER_TYPES.PROJECT]
        )
      }
      if (this.query[FILTER_TYPES.TASK]) {
        remove(
          bookmarks,
          (trw) => trw.task.id !== this.query[FILTER_TYPES.TASK]
        )
      }
      return orderByProjectThenTask(bookmarks)
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
    },
    user () {
      return User.find(this.username)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-bookmarks">
    <app-waiter
      :loader="fetchBookmarksLoader"
      waiter-class="my-5 mx-auto d-block"
    >
      <template v-if="taskRecordReviewIds.length">
        <bookmarks-page-params
          :tasks="tasks"
          :project-id.sync="projectId"
          :task-id.sync="taskId"
        />
        <div
          v-for="(projectValue, name) in bookmarksGroupedByProject"
          :key="name"
          class="user-retrieve-bookmarks__project mt-4 mb-4 border-bottom"
        >
          <h1 class="mb-3 mt-4 text-primary">{{ name }}</h1>
          <div
            v-for="(taskValue, taskName) in bookmarksGroupedByTask(
              projectValue
            )"
            :key="taskName"
            class="user-retrieve-bookmarks__project__task mb-4"
          >
            <div class="d-flex flex-row mb-4 ml-4 mt-4">
              <h2 class="text-tertiary">{{ taskName }}</h2>
            </div>
            <b-list-group-item
              v-for="record in taskValue"
              class="
                user-retrieve-bookmarks__project__task__record
                flex-column
                align-items-start
                ml-4
                border-0
              "
              :key="record.id"
            >
              <task-record-review-card
                :task-record-review-id="record.id"
                :active="true"
              />
            </b-list-group-item>
          </div>
        </div>
      </template>
      <div
        v-else
        class="
          user-retrieve-bookmarks__no-items
          text-center text-secondary text-small
        "
      >
        {{ $t("userRetrieveBookmarks.noBookmarks") }}
      </div>
    </app-waiter>
  </div>
</template>
