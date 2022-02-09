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
  created () {
    // If the notifications were not fetched yet, 
    // we start the component loader
    if (!this.fetched) {
      this.$wait.start(this.loader)
    }
    // Plan notifications polling and fetch them
    this.$store.dispatch('userNotificationsPoll/startPollAndFetch')
  },
  watch: {
    fetched (fetched) {
      // Once the notifications have been fetched,
      // we stop the component loader
      if (fetched) {
        this.$wait.end(this.loader)
      }
    }
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
    },
    fetched () {
      return this.$store.getters['userNotificationsPoll/fetched']
    }
  },
  methods: {
    async markAllAsRead () {
      const ids = this.unreadNotifications.map(n => n.id)
      await UserNotification.api().bulkMarkAsRead(ids)
      this.$store.dispatch('userNotificationsPoll/fetch')
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
      <template v-else-if="fetched">
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
