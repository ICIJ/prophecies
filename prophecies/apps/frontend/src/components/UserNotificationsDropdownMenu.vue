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
    },
    unreadNotifications () {
      return this.notifications.filter(n => !n.read)
    },
    nbUnreadNotifications () {
      return this.unreadNotifications.length
    },
    hasUnreadNotifications () {
      return this.nbUnreadNotifications > 0
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
  <div class="user-notifications-dropdown-menu">
    <app-waiter :loader="loader" waiter-class="my-5 mx-auto d-block">
      <template v-if="notifications.length">
        <b-dropdown-text>
          <h3>Notifications</h3>
        </b-dropdown-text>
        <div class="px-3 text-right user-notifications-dropdown-menu__read_all">
          <b-btn  v-if="hasUnreadNotifications" variant="link" class="btn-sm user-notifications-dropdown-menu__read_all--mark_all" @click="markAllAsRead">
            <check-icon size="1.3x"/><span class="pl-1 align-middle">{{$t('notification.markAll')}} </span>
          </b-btn>
          <b-btn  v-else variant="link" class="btn-sm user-notifications-dropdown-menu__read_all--all_read" disabled >{{$t('notification.allRead')}}</b-btn>
        </div>
        <div class="user-notifications-dropdown-menu__list">
          <div
            v-for="notification in notifications"
            class="user-notifications-dropdown-menu__list__item"
            :class="{ 'user-notifications-dropdown-menu__list__item--read': notification.read }"
            :key="notification.id">
            <b-dropdown-item link-class="user-notifications-dropdown-menu__list__item__link" @click="markAsRead(notification)" :href="notification.link">
              <div class="row">
                <div class="col-10 user-notifications-dropdown-menu__list__item__link__description" v-html="$t(notification.i18n, notification.action)"></div>
                <div v-if="!notification.read" class="d-flex flex-grow-1 align-items-center justify-content-center pr-3">
                  <span class="user-notifications-dropdown-menu__list__item--unread"></span>
                  </div>
              </div>
              <span class="user-notifications-dropdown-menu__list__item__link__created-at text-primary small" :title="notification.createdAt | formatDateLong" v-b-tooltip.bottom>
                {{ notification.createdAt | formatDateFromNow }}
              </span>
            </b-dropdown-item>
          </div>
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
    &__list{
      max-height: 375px;
      overflow: auto;
      &__item {
          //border-top: 1px solid $secondary-50;
          &--read &__link {
            opacity: $btn-disabled-opacity;
          }
          &--unread {
            display: inline-flex;
            z-index: 2;
            width: 14px;
            height: 14px;
            background-color: $danger;
            border-radius: 50%;
          }

          & &__link {
            white-space: normal;
            padding: $spacer $dropdown-item-padding-x;
          }
        }
    }

  }
</style>
