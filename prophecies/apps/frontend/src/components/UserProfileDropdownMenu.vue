<script>
  import AppVersion from './AppVersion.vue'

  export default {
    name: 'UserProfileDropdownMenu',
    components: {
      AppVersion,
    },
    computed: {
      user () {
        return this.$config.get('user')
      }
    }
  }
</script>

<template>
  <div class="user-profile-dropdown-menu">
    <b-dropdown-item :href="$config.get('apiUrl')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--api">
      <code-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('appHeader.api') }}
    </b-dropdown-item>
    <template v-if="user.isStaff">
      <b-dropdown-item :href="$config.get('adminUrl')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--admin">
        <trello-icon class="user-profile-dropdown-menu__item__icon" />
        {{ $t('appHeader.admin') }}
      </b-dropdown-item>
    </template>
    <b-dropdown-item :href="$config.get('helpLink')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--help">
      <truck-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('appHeader.help') }}
    </b-dropdown-item>
    <b-dropdown-item :href="$config.get('logoutUrl')" class="user-profile-dropdown-menu__item user-profile-dropdown-menu__item--logout">
      <log-out-icon class="user-profile-dropdown-menu__item__icon" />
      {{ $t('appHeader.logOut') }}
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