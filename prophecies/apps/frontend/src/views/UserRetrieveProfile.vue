<script>
import { formatDateLongAlt } from '@/utils/date'
import TaskStatus from '@/components/TaskStatus'
import UserAvatar from '@/components/UserAvatar'
import Task from '@/models/Task'
import User from '@/models/User'

export default {
  name: 'UserRetrieveProfile',
  components: {
    TaskStatus,
    UserAvatar
  },
  props: {
    username: {
      type: String
    }
  },
  filters: {
    formatDate (d) {
      return formatDateLongAlt(d)
    },
    isTaskOpen (taskId) {
      return Task.find(taskId)?.open
    }
  },
  data () {
    return {
      assignedTaskIds: []
    }
  },
  async mounted () {
    await this.fetchUserTasks()
  },
  computed: {
    user () {
      return User.find(this.username)
    }
  },
  methods: {
    async fetchUserTasks () {
      const params = { 'filter[checkers]': this.user.id }
      const { entities: { Task: tasks } } = await Task.api().get('', { params })
      this.assignedTaskIds = tasks.map(t => t.id)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-profile" v-if="user">
    <div class="d-flex">
      <div class="pr-4">
        <user-avatar :user-id="user.id" />
      </div>
      <div class="flex-grow-1">
        <h2>{{ user.firstName }} {{ user.lastName }}</h2>
        <p class="font-weight-bold text-muted mb-5">@{{ user.username }}</p>
        <ul class="list-unstyled">
          <li class="mb-3" v-if="user.isSuperuser">
            <span class="d-inline-flex py-0 px-3 bg-warning rounded align-items-center text-primary">
              <award-icon size="1.5x" class="my-2 mr-2" />
              Admin
            </span>
          </li>
          <li class="mb-3">
            Email: <a :href="`mailto:${user.email}`">{{ user.email }}</a>
          </li>
          <li>
            Last login: {{ user.lastLogin | formatDate }}
          </li>
        </ul>
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
  </div>
</template>
