<script>
import { orderBy } from 'lodash'

import { formatDateLongAlt } from '@/utils/date'
import UserTaskStatsCard from '@/components/UserTaskStatsCard'
import UserCard from '@/components/UserCard'
import Task from '@/models/Task'
import User from '@/models/User'
import AdminBadge from '@/components/AdminBadge'
import UserLink from '@/components/UserLink'

export default {
  name: 'UserRetrieveTeam',
  components: {
    UserLink,
    UserCard,
    UserTaskStatsCard,
    AdminBadge
  },
  filters: {
    formatDate(d) {
      return formatDateLongAlt(d)
    },
    isTaskOpen(taskId) {
      return Task.find(taskId)?.open
    }
  },
  props: {
    username: {
      type: String
    }
  },
  data() {
    return {
      teammateIds: []
    }
  },
  computed: {
    currentUser() {
      return User.find(this.username)
    }
  },
  created() {
    this.setup()
  },
  methods: {
    async setup() {
      const tms = await this.fetchUserTasks()
      this.teammateIds = orderBy(tms, ['isSuperuser'], 'desc').map((tm) => tm.id)
    },
    async fetchUserTasks() {
      const params = {
        'filter[checkers]': this.currentUser.id,
        include: 'project,checkers'
      }
      const {
        entities: { User: users }
      } = await Task.api().get('', { params })
      return users.filter((u) => u.id !== this.currentUser.id)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-team container-fluid">
    <div class="row">
      <div v-for="id in teammateIds" :key="id" class="col-12 col-xxl-6 mb-5 px-4">
        <user-card class="user-card-team h-100 p-5" :user-id="id" background>
          <template #header="{ user }">
            <div class="d-flex justify-content-between">
              <div>
                <h2 class="user-card__fullname">{{ user.displayFullName }}</h2>
                <p class="user-card__link font-weight-bold text-muted">
                  <user-link no-card :user-id="user.id" />
                </p>
              </div>
              <div v-if="user.isSuperuser" class="user-retrieve-profile__super-user mb-3">
                <admin-badge />
              </div>
            </div>
          </template>
          <template #footer="{ assignedTaskIds }">
            <user-task-stats-card :user-id="id" :task-ids="assignedTaskIds" />
          </template>
        </user-card>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.user-retrieve-team {
  & .user-card {
    & .user-card__link {
      margin-top: $spacer;
    }

    & ::v-deep .user-card__assigned-tasks__list {
      height: 5rem;
      overflow-y: auto;
      margin-bottom: $spacer-xl;
    }
  }
}
</style>
