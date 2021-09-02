<script>
  import moment from 'moment'
  import { uniqueId } from 'lodash'
  import AppWaiter from '@/components/AppWaiter'
  import Notification from '@/models/Notification'

  export default {
    name: 'NotificationsDropdownMenu',
    components: {
      AppWaiter
    },
    filters: {
      formatDateLong (d) {
        return moment(d).format('MMM Do YYYY - hh:mm')
      },
      formatDateFromNow (d) {
        return moment(d).fromNow()
      }
    },
    created () {
      return this.fetchNotificationsWithLoader()
    },
    computed: {
      loader () {
        return uniqueId('notifications-dropdown-menu-')
      },
      notifications () {
        return Notification
          .query()
          .with('action')
          .with('action.actor')
          .with('action.target')
          .with('action.actionObject')
          .orderBy('createdAt', 'desc')
          .get()
      }
    },
    methods: {
      async fetchNotificationsWithLoader () {
        this.$wait.start(this.loader)
        await this.fetchNotifications()
        this.$wait.end(this.loader)
      },
      fetchNotifications () {
        return Notification.api().get()
      },
      markAsRead (notification) {
        return Notification.api().markAsRead(notification.id)
      }
    }
  }
</script>

<template>
  <div class="notifications-dropdown-menu">
    <app-waiter :loader="loader" waiter-class="my-5 mx-auto d-block">
      <template v-if="notifications.length">
        <b-dropdown-text>
          <h3>Notifications</h3>
        </b-dropdown-text>
        <div
          v-for="notification in notifications"
          class="notifications-dropdown-menu__item"
          :class="{ 'notifications-dropdown-menu__item--read': notification.read }"
          :key="notification.id">
          <b-dropdown-item link-class="notifications-dropdown-menu__item__link" @click="markAsRead(notification)">
            <div class="notifications-dropdown-menu__item__link__description" v-html="$t(notification.i18n, notification.action)"></div>
            <div class="notifications-dropdown-menu__item__link__created-at text-primary small">
              {{ notification.createdAt | formatDateFromNow }}
            </div>
          </b-dropdown-item>
        </div>
      </template>
      <b-dropdown-text v-else class="notifications-dropdown-menu__empty text-muted text-center">
        <div class="text-center p-3 text-muted">
          <bell-icon size="3x" />
        </div>
        <p>
          You don't have any notification yet.
        </p>
      </b-dropdown-text>
    </app-waiter>
  </div>
</template>

<style lang="scss">
  .notifications-dropdown-menu {
    &__item {
      &--read &__link {
        opacity: $btn-disabled-opacity;
      }

      & &__link {
        white-space: normal;
        padding: $spacer $dropdown-item-padding-x;
      }
    }
  }
</style>
