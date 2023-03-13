<script>
import UserNotifications from '@/components/UserNotifications'
import UserNotificationLink from '@/components/UserNotificationLink'
import User from '@/models/User'
import UserNotification from '@/models/UserNotification'

export default {
  name: 'UserNotificationsDropdownMenu',
  components: {
    UserNotifications,
    UserNotificationLink
  },
  beforeCreate() {
    // Plan notifications polling and fetch them
    this.$store.dispatch('userNotificationsPoll/startPollAndFetch')
  },
  computed: {
    notifications() {
      return this.$store.getters['userNotificationsPoll/fetchedObjects']
    },
    notificationIds() {
      return this.$store.getters['userNotificationsPoll/fetchedIds']
    },
    unreadNotifications() {
      return this.notifications.filter(n => !n.read)
    },
    hasUnreadNotifications() {
      return this.unreadNotifications.length > 0
    },
    username() {
      return User.me()?.username
    },
    userNotificationsRoute() {
      const params = {username: this.username}
      return {name: 'user-retrieve-notifications', params}
    }
  },
  methods: {
    async markAllAsRead() {
      const ids = this.unreadNotifications.map(n => n.id)
      await UserNotification.api().bulkMarkAsRead(ids)
      await this.$store.dispatch('userNotificationsPoll/fetch')
    }
  }
}
</script>

<template>
  <div class="user-notifications-dropdown-menu">
    <user-notifications
      class="user-notifications-dropdown-menu__list dropdown"
      :notification-ids="notificationIds">
      <template #header>
        <div class="b-dropdown-text d-flex align-items-center">
          <h3 class="my-2">
            Notifications
          </h3>
          <b-btn
            @click="markAllAsRead"
            :disabled="!hasUnreadNotifications"
            class="user-notifications-dropdown-menu__mark-all ml-auto"
            size="sm"
            variant="link">
            <check-icon size="1.3x"/>
            <span class="pl-1 align-middle">
              {{$t('notification.markAll')}}
            </span>
          </b-btn>
        </div>
      </template>
      <template #link="{ notification }">
        <user-notification-link
          class="dropdown-item py-3"
          :notification-id="notification.id"
          :key="notification.id"/>
      </template>
    </user-notifications>
    <div class="user-notifications-dropdown-menu__footer border-top">
      <b-btn block variant="link" :to="userNotificationsRoute" :disabled="!notifications.length">
        {{$t('notification.seeAllNotifications')}}
      </b-btn>
    </div>
  </div>
</template>

<style lang="scss">
.user-notifications-dropdown-menu {
  &__list {
    max-height: 375px;
    overflow: auto;
  }
}
</style>
