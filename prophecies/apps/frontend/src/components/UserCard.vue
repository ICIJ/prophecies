<script>
  import { uniqueId } from 'lodash'
  import AppWaiter from '@/components/AppWaiter'
  import TaskStatus from '@/components/TaskStatus'
  import UserAvatar from '@/components/UserAvatar'
  import Task from '@/models/Task'
  import User from '@/models/User'

  export default {
    name: 'UserCard',
    components: {
      AppWaiter,
      TaskStatus,
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
      assignedTasks () {
        return Task
          .query()
          .with('project')
          .findIn(this.assignedTaskIds)
      },
      fetchLoader () {
        return uniqueId('fetch-user-card-')
      }
    },
    filters: {
      taskRoute ({ id: taskId }) {
        return {
          name: 'task-record-review-list',
          params: {
            taskId
          }
        }
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
          <div v-if="assignedTasks.length">
            <p>Assigned in:</p>
            <ul>
              <li v-for="task in assignedTasks" :key="task.id" class="mb-2">
                <router-link :to="task | taskRoute" class="font-weight-bold">
                  {{ task.name }}
                </router-link>
                in {{ task.project.name }}
                <task-status :task-id="task.id" class="ml-2" v-if="!task.open" />
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