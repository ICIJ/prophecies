<script>
import { formatDateLongAlt } from '@/utils/date'
import UserCard from '@/components/UserCard'
import Task from '@/models/Task'
import User from '@/models/User'

export default {
  name: 'UserRetrieveTeam',
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
      teammates: []
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
      const params = { 'filter[checkers]': this.user.id, include: 'project,checkers' }
      const { entities: { User: users } } = await Task.api().get('', { params })
      this.teammates = users.filter(u => u.id !== this.user.id)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-team container-fluid">
    <div class="row">
      <div
        class="col-12 col-lg-6 mb-3"
        v-for="{ username } in teammates"
        :key="username"
      >
        <user-card class="user-retrieve-team__user-card" :username="username" background/>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .user-retrieve-team  {
    & /deep/ .user-card__assigned-tasks__list{
          height: 5rem;
          overflow-y: auto;
    }
  }
</style>
