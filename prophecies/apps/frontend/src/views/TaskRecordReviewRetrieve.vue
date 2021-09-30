<script>
  import { find, get, uniqueId } from 'lodash'

  import AppBreadcrumb from '@/components/AppBreadcrumb'
  import AppHeader from '@/components/AppHeader'
  import AppWaiter from '@/components/AppWaiter'
  import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
  import ChoiceGroup from '@/models/ChoiceGroup'
  import Task from '@/models/Task'
  import TaskRecordReview from '@/models/TaskRecordReview'

  export default {
    name: 'TaskRecordReviewRetrieve',
    components: {
      AppBreadcrumb,
      AppHeader,
      AppWaiter,
      TaskRecordReviewCard,
    },
    props: {
      taskId: {
        type: [Number, String]
      },
      taskRecordReviewId: {
        type: [Number, String]
      },
    },
    data () {
      return {
        resolvedTaskRecordReviewId: null
      }
    },
    created () {
      return this.setup()
    },
    watch: {
      taskId () {
        return this.setup()
      },
      taskRecordReviewId () {
        return this.setup()
      }
    },
    computed: {
      fetchAllLoader () {
        return uniqueId('load-task-record-review-retrieve-')
      },
      highlightNote () {
        if (String(this.$route.query.highlightNote).toLowerCase() === 'true') {
          return this.taskRecordReviewId
        }
        return false
      },
      task () {
        return Task
          .query()
          .with('checkers')
          .with('choiceGroup')
          .with('choiceGroup.alternativeValues')
          .with('choiceGroup.choices')
          .find(this.taskId)
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
      async fetchAll () {
        await this.fetchTaskOnce()
        await this.fetchChoiceGroup()
        await this.fetchTaskRecordReview()
      },
      async fetchTaskOnce () {
        if (!Task.find(this.taskId)) {
          return Task.api().find(this.taskId)
        }
      },
      async fetchChoiceGroup () {
        return ChoiceGroup.api().find(this.task.choiceGroupId)
      },
      async fetchTaskRecordReview () {
        // User might try to access a TaskRecordReview assigned to another user.
        // We need to find the id of the review assigned to the current user.
        const params = { 'filter[task_record__reviews__id]': this.taskRecordReviewId }
        const { response } = await TaskRecordReview.api().get('', { params })
        const reviews = get(response, 'data.data', [])
        const userReviewId = find(reviews, ({ id }) => TaskRecordReview.find(id)?.editable)?.id || null
        // In case we didn't a task record review a user can edit, 
        // we just use the first one from the list
        const firstReviewId = reviews[0]?.id || null
        this.resolvedTaskRecordReviewId = userReviewId || firstReviewId
      },
      async waitFor (loader, fn) {
        this.$wait.start(loader)
        await fn()
        this.$wait.end(loader)
      }
    }
  }
</script>

<template>
  <div class="task-record-review-retrieve">
    <div class="d-flex align-items-center">
      <app-breadcrumb v-if="task">
        <template #items>
          <li class="list-inline-item app-breadcrumb__item">
            <router-link :to="{ name: 'task-record-review-list', params: { taskId: task.id } }">
              {{ task.name }}
            </router-link>
          </li>
          <li class="list-inline-item app-breadcrumb__item">
            {{ taskRecordReviewId }}
          </li>
        </template>
      </app-breadcrumb>
      <app-header class="flex-grow-1" />
    </div>
    <div class="task-record-review-retrieve__container">
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchAllLoader" waiter-class="my-5 mx-auto d-block">
          <template v-if="resolvedTaskRecordReviewId">
            <task-record-review-card
              active
              :highlight-note="highlightNote"
              :task-record-review-id="resolvedTaskRecordReviewId" />
          </template>
          <div v-else class="text-center text-muted text-small mx-auto">
            Unable to find this resource.
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>
