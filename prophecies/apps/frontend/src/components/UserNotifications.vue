<script>
import { uniqueId } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import UserNotificationLink from '@/components/UserNotificationLink'
import UserNotification from '@/models/UserNotification'

export default {
  name: 'UserNotifications',
  components: {
    AppWaiter,
    UserNotificationLink
  },
  data () {
    return {
      planFetchNotificationsId: null
    }
  },
  async created () {
    await this.fetchNotificationsWithLoader()
    this.planFetchNotifications()
  },
  beforeDestroy () {
    clearInterval(this.planFetchNotificationsId)
  },
  computed: {
    loader () {
      return uniqueId('user-notifications-')
    },
    notifications () {
      return UserNotification
        .query()
        .orderBy('createdAt', 'desc')
        .get()
    },
    unreadNotifications () {
      return this.notifications.filter(n => !n.read)
    },
    hasUnreadNotifications () {
      return this.unreadNotifications.length > 0
    }
  },
  methods: {
    async fetchNotificationsWithLoader () {
      this.$wait.start(this.loader)
      await this.fetchNotifications()
      this.$wait.end(this.loader)
    },
    fetchNotifications () {
      const pageSize = 50
      const include = 'action.actionObject'
      const params = { 'page[size]': pageSize, include }
      return UserNotification.api().get('', { params })
    },
    planFetchNotifications () {
      this.planFetchNotificationsId = setInterval(this.fetchNotifications, 1e4)
    },
    async markAllAsRead () {
      const ids = this.unreadNotifications.map(n => n.id)
      await UserNotification.api().bulkMarkAsRead(ids)
      await this.fetchNotifications()
    }
  }
}
</script>

<template>
  <div class="user-notifications">
    <app-waiter :loader="loader" waiter-class="my-5 mx-auto d-block">
      <slot name="header" />
      <template v-if="notifications.length">
        <div class="user-notifications__list">
          <template v-for="notification in notifications">
            <slot name="link" v-bind="{ notification }">
              <user-notification-link :notification-id="notification.id" :key="notification.id" />
            </slot>
          </template>
        </div>
      </template>
      <template v-else>
        <div  class="user-notifications__empty text-muted text-center">
          <div class="text-center p-3 text-muted">
            <bell-icon size="3x" />
          </div>
          <p>
            You don't have any notification yet.
          </p>
        </div>
      </template>
      <slot name="footer" />
    </app-waiter>
  </div>
</template>
