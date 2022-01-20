<script>
import { template } from 'lodash'
import store from '@/store'
import UserNotification from '@/models/UserNotification'
import AppSearchForm from '@/components/AppSearchForm'
import AppVersion from '@/components/AppVersion'
import UserNotificationsDropdownMenu from '@/components/UserNotificationsDropdownMenu'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import ShortcutListCard from '@/components/ShortcutListCard'
import UserProfileDropdownMenu from '@/components/UserProfileDropdownMenu.vue'

export default {
  name: 'AppHeader',
  components: {
    AppSearchForm,
    AppVersion,
    UserNotificationsDropdownMenu,
    ShortkeyBadge,
    ShortcutListCard,
    UserProfileDropdownMenu
  },
  props: {
    reduced: {
      type: Boolean
    },
    tipQueryParams: {
      type: Object,
      default: () => {}
    }
  },
  created () {
    const showTutorial = this.showTutorial !== false
    if (showTutorial !== this.showTutorial) {
      store.dispatch('app/showTutorial', showTutorial)
    }
  },
  methods: {
    toggleTutorial () {
      this.showTutorial = !this.showTutorial
    },
    toggleCinematicView () {
      this.$root.$emit('prophecies::toggleCinematicView')
    },
    toggleShortcuts () {
      this.$root.$emit('prophecies::toggleShortcuts')
    },
    toggleTips () {
      this.$root.$emit('prophecies::toggleTips')
    }
  },
  computed: {
    user () {
      return this.$config.get('user')
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
      return UserNotification.query().where('read', false).count()
    },
    showTutorial: {
      get () {
        return store.state.app.showTutorial
      },
      set (isVisible) {
        store.dispatch('app/showTutorial', isVisible)
      }
    }
  }
}
</script>

<template>
  <b-navbar toggleable="lg" class="app-header py-3">
    <b-navbar-toggle target="nav-collapse" class="ml-auto" />
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="app-header__nav-left flex-grow-1">
        <slot name="nav-left" />
        <app-search-form is-nav class="app-header__nav-left__search-form" />
      </b-navbar-nav>
      <div class="ml-auto">
        <b-navbar-nav class="app-header__nav-right">
          <slot name="nav-right" />
          <template v-if="!reduced">
            <b-nav-item @click.prevent="toggleCinematicView">
              <film-icon class="mr-2" />
              {{ $t('appHeader.cinematicView') }}
            </b-nav-item>
            <b-nav-item @click.prevent="toggleShortcuts">
              <command-icon class="mr-2" />
              {{ $t('appHeader.shortcuts') }}
              <shortkey-badge :value="['Ctrl', 'k']" class="ml-2" />
            </b-nav-item>
            <b-nav-item @click.prevent="toggleTips">
              <smile-icon class="app-header__nav-right__tips mr-2" />
              {{ $t('appHeader.tips') }}
              <shortkey-badge :value="['Ctrl', 'Shift', 't']" class="ml-2" />
            </b-nav-item>
            <b-nav-item
              :class="{ 'font-weight-bold app-header__nav-right__tutorial--show': showTutorial }"
              @click="toggleTutorial"
              href="#">
              <help-circle-icon class="mr-2" />
              {{ $t('appHeader.tutorial') }}
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
                {{ user.displayFullName }}
              </span>
              <img :src="userAvatarUrl" class="app-header__nav-right__user__avatar rounded-circle ml-2 d-none d-lg-inline" height="42" width="42" />
            </template>
            <user-profile-dropdown-menu />
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </div>
    </b-collapse>
  </b-navbar>
</template>

<style lang="scss" scoped>
  .app-header {

    &__nav-left {
      width: 100%;

      & /deep/ &__search-form {
        width: 100%;
      }
    }

    & /deep/ .nav-item .nav-link .feather,
    & /deep/ .navbar-text .feather,
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

    & /deep/ &__nav-right .nav-link {
      white-space: nowrap;
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

    & /deep/ &__nav-right__tutorial  {
      &--show.nav-item .nav-link {
        color: $primary;
        margin-left: -3px; /* hack to prevent layout shift when the fond is bold */
      }
    }
  }
</style>
