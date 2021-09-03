<script>
  import { template } from 'lodash'
  import UserNotification from '@/models/UserNotification'
  import UserNotificationsDropdownMenu from '@/components/UserNotificationsDropdownMenu'
  import ShortkeyBadge from '@/components/ShortkeyBadge'

  export default {
    name: 'AppHeader',
    components: {
      UserNotificationsDropdownMenu,
      ShortkeyBadge
    },
    props: {
      reduced: {
        type: Boolean
      }
    },
    computed: {
      user () {
        return this.$config.get('user')
      },
      userDisplayName () {
        if (!this.user.firstName || !this.user.lastName) {
          return this.user.username
        }
        return `${this.user.firstName} ${this.user.lastName}`
      },
      userAvatarUrl () {
        const interpolate = this.$config.get('templateInterpolate')
        const avatarUrlTemplate = this.$config.get('avatarUrlTemplate')
        const compiled = template(avatarUrlTemplate, { interpolate })
        return compiled(this.user)
      },
      hasUnreadNotifications () {
        return this.unreadNotifications > 0
      },
      unreadNotifications () {
        return UserNotification.query().where('read', false ).count()
      }
    }
  }
</script>

<template>
  <b-navbar toggleable="lg" class="app-header py-3">
    <b-navbar-toggle target="nav-collapse" class="ml-auto" />
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="app-header__nav-left">
        <slot name="nav-left" />
        <b-nav-item href="#">
          <search-icon class="mr-2" />
          {{ $t('appHeader.search') }}
          <shortkey-badge :value="['meta', 'f']" class="ml-2" />
        </b-nav-item>
      </b-navbar-nav>
      <div class="ml-auto">
        <b-navbar-nav class="app-header__nav-right">
          <slot name="nav-right" />
          <template v-if="!reduced">
            <b-nav-item href="#">
              <smile-icon class="app-header__nav-right__tips mr-2" />
              <router-link :to="{ name: 'tip-list' }">
                {{ $t('appHeader.tips') }}
              </router-link>
              <shortkey-badge :value="['meta', 't']" class="ml-2" />
            </b-nav-item>
            <b-nav-item href="#">
              <command-icon class="app-header__nav-right__shortcuts mr-2" />
              {{ $t('appHeader.shortcuts') }}
              <shortkey-badge :value="['meta', 'k']" class="ml-2" />
            </b-nav-item>
          </template>
          <b-nav-item-dropdown
            right
            no-caret
            class="app-header__nav-right__notifications"
            :class="{ 'app-header__nav-right__notifications--unread': hasUnreadNotifications }"
            toggle-class="app-header__nav-right__notifications__toggler"
            menu-class="app-header__nav-right__notifications__menu">
            <template #button-content>
              <bell-icon />
              <b-badge variant="danger" v-if="hasUnreadNotifications" pill class="app-header__nav-right__notifications__toggler__count">
                {{ unreadNotifications }}
              </b-badge>
            </template>
            <user-notifications-dropdown-menu />
          </b-nav-item-dropdown>
          <b-nav-item-dropdown right no-caret class="app-header__nav-right__user" toggle-class="pl-1">
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <span class="app-header__nav-right__user__display-name">
                {{ userDisplayName }}
              </span>
              <img :src="userAvatarUrl" class="app-header__nav-right__user__avatar rounded-circle ml-2 d-none d-lg-inline" height="42" width="42" />
            </template>
            <b-dropdown-item :href="$config.get('apiUrl')" class="app-header__nav-right__user__api">
              <code-icon class="mr-2" />
              {{ $t('appHeader.api') }}
            </b-dropdown-item>
            <template v-if="user.isStaff">
              <b-dropdown-item :href="$config.get('adminUrl')" class="app-header__nav-right__user__admin">
                <trello-icon class="mr-2" />
                {{ $t('appHeader.admin') }}
              </b-dropdown-item>
              <b-dropdown-divider />
            </template>
            <b-dropdown-item :href="$config.get('logoutUrl')" class="app-header__nav-right__user__logout">
              <log-out-icon class="mr-2" />
              {{ $t('appHeader.logOut') }}
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
        </slot>
      </div>
    </b-collapse>
  </b-navbar>
</template>

<style lang="scss" scoped>
  .app-header {

    & /deep/ .nav-item .nav-link .feather,
    & /deep/ .dropdown-item .feather {
      height: 20px;
      width: 20px
    }

    & /deep/ .nav-item,
    & /deep/ .nav-item .nav-link,
    & /deep/ .nav-item .dropdown-toggle {
      display: flex;
      align-items: center;
    }

    & /deep/ &__nav-right__notifications__menu {
      width: 360px;
    }

    & /deep/ &__nav-right__notifications__toggler {
      position: relative;
    }

    & /deep/ &__nav-right__notifications--unread &__nav-right__notifications__toggler {
      color: $danger;
    }

    & /deep/ &__nav-right__notifications__toggler__count {
      position: absolute;
      top: 0;
      right: $spacer;
    }
  }
</style>
