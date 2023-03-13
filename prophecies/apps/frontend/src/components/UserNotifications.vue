<script>
import {uniqueId} from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import UserNotificationLink from '@/components/UserNotificationLink'
import EmptyPlaceholder from '@/components/EmptyPlaceholder'
import UserNotification from '@/models/UserNotification'

export default {
  name: 'UserNotifications',
  components: {
    AppWaiter,
    UserNotificationLink,
    EmptyPlaceholder
  },
  props: {
    notificationIds: {
      type: Array,
      default: () => ([])
    },
    fetching: {
      type: Boolean
    }
  },
  created() {
    // If the notifications were not fetched yet,
    // we start the component loader
    if (this.fetching) {
      this.$wait.start(this.loader)
    }
  },
  watch: {
    fetching(fetching) {
      // Once the notifications have been fetched,
      // we stop the component loader
      if (!fetching) {
        this.$wait.end(this.loader)
      }
    }
  },
  computed: {
    loader() {
      return uniqueId('user-notifications-')
    },
    notifications() {
      return UserNotification
        .query()
        .whereIdIn(this.notificationIds)
        .orderBy('createdAt', 'desc')
        .get()
    },
    unreadNotifications() {
      return this.notifications.filter(n => !n.read)
    },
    hasUnreadNotifications() {
      return this.unreadNotifications.length > 0
    }
  },
  methods: {
    async markAllAsRead() {
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
      <slot name="header"/>
      <template v-if="notifications.length">
        <div class="user-notifications__list">
          <template v-for="notification in notifications">
            <slot name="link" v-bind="{ notification }">
              <user-notification-link :notification-id="notification.id" :key="notification.id"/>
            </slot>
          </template>
        </div>
      </template>
      <template v-else>
        <empty-placeholder class="user-notifications__empty" icon="BellIcon"
                           :title="$t('userNotifications.noNotification')"/>
      </template>
      <slot name="footer"/>
    </app-waiter>
  </div>
</template>
