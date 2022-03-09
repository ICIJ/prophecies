<script>
import AppVersion from './AppVersion.vue'

export default {
  name: 'UserProfileDropdownMenu',
  components: {
    AppVersion
  },
  computed: {
    user () {
      return this.$config.get('user')
    },
    userRoute () {
      const params = { username: this.user.username }
      return { name: 'user-retrieve-profile', params }
    },
    activityRoute () {
      const params = { username: this.user.username }
      return { name: 'user-retrieve-activity', params }
    },
    notificationsRoute () {
      const params = { username: this.user.username }
      return { name: 'user-retrieve-notifications', params }
    },
    teamRoute () {
      const params = { username: this.user.username }
      return { name: 'user-retrieve-team', params }
    },
    bookmarksRoute () {
      const params = { username: this.user.username }
      return { name: 'user-retrieve-bookmarks', params }
    },
    historyRoute () {
      const params = { username: this.user.username }
      return { name: 'user-retrieve-history', params }
    }
  }
}
</script>

<template>
  <div class="user-profile-dropdown-menu">
    <b-dropdown-item :to="userRoute" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--profile">
      <user-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userRetrieveProfile.title.yours') }}
    </b-dropdown-item>
    <b-dropdown-item :to="activityRoute" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--activity">
      <activity-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userRetrieveActivity.title.yours') }}
    </b-dropdown-item>
    <b-dropdown-item :to="notificationsRoute" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--notifications">
      <bell-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userRetrieveNotifications.title.yours') }}
    </b-dropdown-item>
    <b-dropdown-item :to="bookmarksRoute" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--bookmarks">
      <bookmark-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userRetrieveBookmarks.title.yours') }}
    </b-dropdown-item>
    <b-dropdown-item :to="historyRoute" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--history">
      <clock-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userRetrieveHistory.title.yours') }}
    </b-dropdown-item>
    <b-dropdown-item :to="teamRoute" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--team">
      <users-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userRetrieveTeam.title.yours') }}
    </b-dropdown-item>
    <b-dropdown-item :href="$config.get('apiUrl')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--api">
      <code-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userProfileDropdownMenu.api') }}
    </b-dropdown-item>
    <template v-if="user.isStaff">
      <b-dropdown-item :href="$config.get('adminUrl')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--admin">
        <trello-icon class="user-profile-dropdown-menu__item__icon" />
        {{ $t('userProfileDropdownMenu.admin') }}
      </b-dropdown-item>
    </template>
    <b-dropdown-item :href="$config.get('helpLink')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--help">
      <truck-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userProfileDropdownMenu.help') }}
    </b-dropdown-item>
    <b-dropdown-item :href="$config.get('logoutUrl')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--logout">
      <log-out-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('userProfileDropdownMenu.logOut') }}
    </b-dropdown-item>
    <b-dropdown-divider />
    <b-dropdown-text class="small text-center p-0 text-muted">
      <app-version />
    </b-dropdown-text>
  </div>
</template>

<style lang="scss">
  .user-profile-dropdown-menu {
    &__item {
      min-width: 235px;

      a {
        padding: $spacer-sm $spacer-lg;
      }

      &__icon {
        margin-right: $spacer;
      }
    }
  }
</style>
