<script>
import {formatDateFromNow, formatDateLong} from '@/utils/date'
import UserNotification from '@/models/UserNotification'

export default {
  name: 'UserNotificationLink',
  props: {
    notificationId: {
      type: [String, Number]
    }
  },
  filters: {
    formatDateLong(d) {
      return formatDateLong(d)
    },
    formatDateFromNow(d) {
      return formatDateFromNow(d)
    }
  },
  methods: {
    markAsRead() {
      return UserNotification.api().markAsRead(this.notificationId)
    }
  },
  computed: {
    notification() {
      return UserNotification
        .query()
        .with('action')
        .with('action.*')
        .with('action.target.*')
        .with('action.actionObject.*')
        .whereId(this.notificationId)
        .first()
    }
  }
}
</script>

<template>
  <a class="user-notification-link"
     :class="{ 'user-notification-link--read': notification.read }"
     :href="notification.link"
     @click="markAsRead()">
    <div class="row">
      <div class="col-10 user-notification-link__description" v-html="$t(notification.i18n, notification.action)"></div>
      <div v-if="!notification.read" class="d-flex flex-grow-1 align-items-center justify-content-center pr-3">
        <span class="user-notification-link__unread-bullet"></span>
      </div>
    </div>
    <span class="user-notification-link__created-at text-primary small" :title="notification.createdAt | formatDateLong"
          v-b-tooltip.bottom>
      {{ notification.createdAt | formatDateFromNow }}
    </span>
  </a>
</template>

<style lang="scss">
.user-notification-link {
  display: block;
  white-space: normal;
  padding: $spacer;

  &--read {
    opacity: $btn-disabled-opacity;
  }

  &__unread-bullet {
    display: inline-flex;
    z-index: 2;
    width: 14px;
    height: 14px;
    background-color: $danger;
    border-radius: 50%;
  }
}
</style>
