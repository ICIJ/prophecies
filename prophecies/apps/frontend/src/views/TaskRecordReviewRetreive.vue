<script>
  import { uniqueId } from 'lodash'

  import AppBreadcrumb from '@/components/AppBreadcrumb'
  import AppHeader from '@/components/AppHeader'
  import AppWaiter from '@/components/AppWaiter'
  import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'
  import ChoiceGroup from '@/models/ChoiceGroup'
  import Task from '@/models/Task'
  import TaskRecordReview from '@/models/TaskRecordReview'

  export default {
    name: 'TaskRecordReviewRetreive',
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
    computed: {
      fetchAllLoader () {
        return uniqueId('load-task-record-review-retreive-')
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
    created () {
      return this.setup()
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
        await this.fetchTask()
        await this.fetchChoiceGroup()
        await this.fetchTaskRecordReview()
      },
      fetchTask () {
        return Task.api().find(this.taskId)
      },
      fetchChoiceGroup () {
        return ChoiceGroup.api().find(this.task.choiceGroupId)
      },
      fetchTaskRecordReview () {
        return TaskRecordReview.api().find(this.taskRecordReviewId)
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
  <div class="task-record-review-retreive">
    <div class="d-flex align-items-center">
      <app-breadcrumb v-if="task">
        {{ task.name }}
      </app-breadcrumb>
      <app-header class="flex-grow-1" />
    </div>
    <div class="task-record-review-retreive__container">
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchAllLoader" waiter-class="my-5 mx-auto d-block">
          <task-record-review-card :task-record-review-id="taskRecordReviewId" active />
        </app-waiter>
      </div>
    </div>
  </div>
</template>
