<script>
import { uniqueId } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import TaskListItem from '@/components/TaskListItem'
import UserAvatar from '@/components/UserAvatar'
import Task from '@/models/Task'
import User from '@/models/User'

export default {
  name: 'UserCard',
  components: {
    AppWaiter,
    TaskListItem,
    UserAvatar,
    // UserLink is a recursive component
    UserLink: () => import('@/components/UserLink')
  },
  props: {
    userId: {
      type: [String, Number]
    }
  },
  data () {
    return { 
      assignedTaskIds: []
    }
  },
  async created () {
    await this.fetchWithLoader()
  },
  computed: {
    user () {
      return User.find(this.userId)
    },
    fetchLoader () {
      return uniqueId('fetch-user-card-')
    }
  },
  filters: {
    isTaskOpen (taskId) {
      return Task.find(taskId)?.open
    }
  },
  methods: {
    async fetch () {
      const params = { 'filter[checkers]': this.user.id }
      const { entities: { Task: tasks } } = await Task.api().get('', { params })
      this.assignedTaskIds = tasks.map(t => t.id)
    },
    async fetchWithLoader () {
      this.$wait.start(this.fetchLoader)
      await this.fetch()
      this.$wait.end(this.fetchLoader)
    }
  }
}
</script>

<template>
  <div class="user-card" v-if="user">
    <app-waiter :loader="fetchLoader">
      <div class="d-flex">
        <div class="pr-4">
          <user-avatar :user-id="userId" />
        </div>
        <div class="flex-grow-1">
          <h2>{{ user.firstName }} {{ user.lastName }}</h2>
          <p>
            <user-link class="font-weight-bold text-muted" no-card :user-id="userId" />
          </p>
          <div v-if="assignedTaskIds.length">
            <p>Assigned in:</p>
            <ul>
              <li v-for="taskId in assignedTaskIds" :key="taskId" class="mb-2">
                <task-list-item :task-id="taskId" :no-status="taskId | isTaskOpen" />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </app-waiter>
  </div>
</template>

<style lang="scss" scoped>
  .user-card {
    background: $primary-10;
    padding: $spacer-xl;
    font-size: 1rem;
    min-width: 100%;
    width: 530px;
    max-width: 90vw;
    border-radius: $border-radius;
    box-shadow: $box-shadow-sm;
  }
</style>