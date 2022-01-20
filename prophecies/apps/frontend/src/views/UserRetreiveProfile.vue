<script>
import moment from 'moment'
import TaskStatus from '@/components/TaskStatus'
import UserAvatar from '@/components/UserAvatar'
import Task from '@/models/Task'
import User from '@/models/User'

export default {
  name: 'UserRetreiveProfile',
  components:  {
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
      return moment(d).format('ddd DD, MMM YYYY - h:MMa')
    },
    taskRoute ({ id: taskId }) {
      return {
        name: 'task-record-review-list',
        params: {
          taskId
        }
      }
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
      return User.query().where('username', this.username).first()
    },
    assignedTasks () {
      return Task
        .query()
        .with('project')
        .findIn(this.assignedTaskIds)
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
  <div class="user-retreive-profile" v-if="user">
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
  </div>
</template>
