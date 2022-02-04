<script>
import { formatDateLongAlt } from '@/utils/date'
import Task from '@/models/Task'
import User from '@/models/User'
import UserCard from '@/components/UserCard.vue'

export default {
  name: 'UserRetrieveProfile',
  components: {
    UserCard
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
  <user-card :username="username" >
    <template #content :user={user}>
      <ul class="list-unstyled mt-5" >
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
    </template>
  </user-card>
</template>
