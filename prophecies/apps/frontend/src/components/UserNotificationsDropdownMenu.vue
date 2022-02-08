<script>
import UserNotifications from '@/components/UserNotifications'
import UserNotificationLink from '@/components/UserNotificationLink'
import UserNotification from '@/models/UserNotification'

export default {
  name: 'UserNotificationsDropdownMenu',
  components: {
    UserNotifications,
    UserNotificationLink,
    UserNotifications
  },
  computed: {
    notifications () {
      return UserNotification
        .query()
        .with('action')
        .with('action.*')
        .with('action.target.*')
        .with('action.actionObject.*')
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
    async markAllAsRead () {
      const ids = this.unreadNotifications.map(n => n.id)
      await UserNotification.api().bulkMarkAsRead(ids)
      await this.fetchNotifications()
    }
  }
}
</script>

<template>
  <div class="user-notifications-dropdown-menu">
    <user-notifications class="user-notifications-dropdown-menu__list dropdown">
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
          :key="notification.id" />
      </template>
    </user-notifications>
  </div>
</template>

<style lang="scss">
  .user-notifications-dropdown-menu {
    &__list{
      max-height: 375px;
      overflow: auto;
    }
  }
</style>
