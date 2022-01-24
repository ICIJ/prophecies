<script>
import {get, groupBy, uniqueId} from "lodash"

import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
import User from '@/models/User'
import TaskRecordReview from '@/models/TaskRecordReview'

const FILTER_TYPES = {
  PROJECT: 'filter[project]',
  TASK: 'filter[task]',
  CREATOR: 'filter[creator]'
}

export default {
  name: 'Bookmarks',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter,
    TaskRecordReviewCard
  },
  props: {
    query: {
      type: Object,
      default: () => ({
        [FILTER_TYPES.PROJECT]: null,
        [FILTER_TYPES.TASK]: null,
        [FILTER_TYPES.CREATOR]: null
      })
    }
  },
  created() {
    return this.setup()
  },
  computed: {
    fetchBookmarksLoader () {
      return uniqueId('load-bookmarks-')
    },
    bookmarks () {
      return TaskRecordReview
        .query()
        .with('project')
        .with('task')
        .with('taskRecord')
        .get()
    },
    filteredBookmarks () {
      let bookmarks = this.bookmarks.slice()
      if (this.query[FILTER_TYPES.PROJECT]) bookmarks = bookmarks.filter(t => t.projectId === this.query[FILTER_TYPES.PROJECT])
      if (this.query[FILTER_TYPES.TASK]) bookmarks = bookmarks.filter(t => t.taskId === this.query[FILTER_TYPES.TASK])
      return bookmarks.sort(this.sortBookmarksByProjectAndTask)
    },
    bookmarksGroupedByProject () {
      return groupBy(this.filteredBookmarks, (record) => {
        return record.task.project ? record.task.project.name : ''
      })
    },
    taskRecordReviewsParams () {
      return {
        'filter[task_record__bookmarked_by]': User.me().id
      }
    }
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchBookmarksLoader, this.fetchBookmarks)
      } catch (error) {
        const title = 'Unable to retrieve the bookmarks'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    async fetchBookmarks() {
      const params = this.taskRecordReviewsParams
      return TaskRecordReview.api().get('', { params })
    },
    bookmarksGroupedByTask (records) {
      return groupBy(records, (record) => {
        return record.task ? record.task.name : ''
      })
    },
    sortBookmarksByProjectAndTask (a, b) {
      if (!a.project) { return -1 }
      if (!b.project) { return 1 }
      const projectSort = a.project?.name.localeCompare(b.project?.name)
      if (projectSort !== 0) {
        return projectSort
      } else {
        if (!a.task) { return -1 }
        if (!b.task) { return 1 }
        return (a.task?.name.localeCompare(b.task?.name))
      }
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
