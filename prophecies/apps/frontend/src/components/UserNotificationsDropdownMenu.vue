<script>
  import moment from 'moment'
  import { uniqueId } from 'lodash'
  import AppWaiter from '@/components/AppWaiter'
  import UserNotification from '@/models/UserNotification'

  export default {
    name: 'UserNotificationsDropdownMenu',
    components: {
      AppWaiter
    },
    data () {
      return {
        planFetchNotificationsId: null
      }
    },
    filters: {
      formatDateLong (d) {
        return moment(d).format('MMM Do YYYY - hh:mm')
      },
      formatDateFromNow (d) {
        return moment(d).fromNow()
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
        return uniqueId('user-notifications-dropdown-menu-')
      },
      notifications () {
        return UserNotification
          .query()
          .with('action')
          .with('action.*')
          .with('action.target.*')
          .with('action.actionObject.*')
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
        const pageSize = 50
        const include = 'action.actionObject'
        const params = { 'page[size]': pageSize, include }
        return UserNotification.api().get('', { params })
      },
      planFetchNotifications () {
        this.planFetchNotificationsId = setInterval(this.fetchNotifications, 1e4)
      },
      markAsRead (notification) {
        return UserNotification.api().markAsRead(notification.id)
      }
    }
  }
</script>

<template>
  <div class="user-notifications-dropdown-menu">
    <app-waiter :loader="loader" waiter-class="my-5 mx-auto d-block">
      <template v-if="notifications.length">
        <b-dropdown-text>
          <h3>Notifications</h3>
        </b-dropdown-text>
        <div
          v-for="notification in notifications"
          class="user-notifications-dropdown-menu__item"
          :class="{ 'user-notifications-dropdown-menu__item--read': notification.read }"
          :key="notification.id">
          <b-dropdown-item link-class="user-notifications-dropdown-menu__item__link" @click="markAsRead(notification)" :href="notification.link">
            <div class="user-notifications-dropdown-menu__item__link__description" v-html="$t(notification.i18n, notification.action)"></div>
            <div class="user-notifications-dropdown-menu__item__link__created-at text-primary small">
              {{ notification.createdAt | formatDateFromNow }}
            </div>
          </b-dropdown-item>
        </div>
      </template>
      <b-dropdown-text v-else class="user-notifications-dropdown-menu__empty text-muted text-center">
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
  .user-notifications-dropdown-menu {
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
