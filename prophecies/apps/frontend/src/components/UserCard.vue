<script>
import {uniqueId} from 'lodash'
import {formatDateLongAlt} from '@/utils/date'
import AppWaiter from '@/components/AppWaiter'
import TaskListItem from '@/components/TaskListItem'
import UserAvatar from '@/components/UserAvatar'
import Task, {TaskStatusEnum} from '@/models/Task'
import User from '@/models/User'
import {orderTasks} from '@/utils/sort'

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
      type: [String, Number],
      default: undefined
    },
    username: {
      type: String,
      default: undefined
    },
    background: {
      type: Boolean,
      default: false
    }
  },
  filters: {
    formatDate(d) {
      return formatDateLongAlt(d)
    },
    isTaskOpen(taskId) {
      return Task.find(taskId)?.open
    }
  },
  data() {
    return {
      errorMessage: '',
      assignedTaskIds: []
    }
  },
  computed: {
    user() {
      const id = this.userId ?? this.username
      return User.find(id)
    },
    fetchLoader() {
      return uniqueId('fetch-user-card-')
    }
  },
  created() {
    this.setup()
  },
  methods: {
    async setup() {
      await this.waitFor(this.fetchLoader, this.fetchUserTasks)
    },
    async fetchUserTasks() {
      const params = {'filter[checkers]': this.user.id}
      try {
        const {entities: {Task: tasks}} = await Task.api().get('', {params})
        this.errorMessage = ''
        this.assignedTaskIds = orderTasks(tasks)
          .filter(t => t.status !== TaskStatusEnum.CLOSED && t.taskRecordsCount > 0)
          .map(t => t.id)
      } catch (error) {
        this.errorMessage = 'Sorry, this profile is no longer available.'
        this.assignedTaskIds = []
      }
    },
    async waitFor(loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    }
  }
}
</script>

<template>
  <div class="user-card" :class="{'user-card--with-background':background}" v-if="user">
    <app-waiter :loader="fetchLoader">
      <div v-if="errorMessage.length">{{errorMessage}}</div>
      <div v-else class="d-flex">
        <div class="pr-4">
          <user-avatar :user-id="user.id"/>
        </div>
        <div class="flex-grow-1">
          <slot name="header" :user="user">
            <h2 class="user-card__fullname">{{ user.displayFullName }}</h2>
            <p class="user-card__link font-weight-bold text-muted">
              <user-link no-card :user-id="user.id"/>
            </p>
          </slot>
          <slot name="content" :user="user"></slot>
          <div class="user-card__assigned-tasks" v-if="assignedTaskIds.length">
            <p>{{ $tc('userCard.assignedTasks', assignedTaskIds.length) }}</p>
            <ul class="user-card__assigned-tasks__list">
              <li v-for="taskId in assignedTaskIds" :key="taskId" class="mb-2">
                <task-list-item :task-id="taskId" :no-status="taskId | isTaskOpen"/>
              </li>
            </ul>
          </div>
          <slot name="footer" v-bind:assignedTaskIds="assignedTaskIds"></slot>
        </div>
      </div>
    </app-waiter>
  </div>
</template>

<style lang="scss" scoped>
.user-card {
  min-height: 140px;

  &--with-background {
    background: $primary-10;
    padding: $spacer-xl;
    border-radius: $border-radius;
    box-shadow: $box-shadow-sm;
  }

}
</style>
