<script>
  import { template } from 'lodash'
  import ShortkeyBadge from '@/components/ShortkeyBadge'

  export default {
    name: 'AppHeader',
    components: {
      ShortkeyBadge
    },
    computed: {
      user () {
        return this.$config.get('user')
      },
      userDisplayName () {
        if (!this.user.first_name || !this.user.last_name) {
          return this.user.username
        }
        return `${this.user.first_name} ${this.user.last_name}`
      },
      userAvatarUrl () {
        const interpolate = this.$config.get('templateInterpolate')
        const avatarUrlTemplate = this.$config.get('avatarUrlTemplate')
        const compiled = template(avatarUrlTemplate, { interpolate })
        return compiled(this.user)
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
      </b-navbar-nav>
      <div class="ml-auto" >
        <b-navbar-nav class="app-header__nav-right">
          <slot name="nav-right" />
          <b-nav-item href="#">
            <search-icon size="1x" class="mr-2" />
            {{ $t('appHeader.search') }}
            <shortkey-badge :value="['meta', 'f']" class="ml-2" />
          </b-nav-item>
          <b-nav-item href="#">
            <smile-icon size="1x" class="app-header__nav-right__tips mr-2" />
            {{ $t('appHeader.tips') }}
            <shortkey-badge :value="['meta', 't']" class="ml-2" />
          </b-nav-item>
          <b-nav-item href="#">
            <command-icon size="1x" class="app-header__nav-right__shortcuts mr-2" />
            {{ $t('appHeader.shortcuts') }}
            <shortkey-badge :value="['meta', 'k']" class="ml-2" />
          </b-nav-item>
          <b-nav-item-dropdown right no-caret class="app-header__nav-right__user">
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <bell-icon size="1x" class="mr-2" />
              <span class="app-header__nav-right__user__display-name">
                {{ userDisplayName }}
              </span>
              <img :src="userAvatarUrl" class="app-header__nav-right__user__avatar rounded-circle ml-2 d-none d-lg-inline" height="42" width="42" />
            </template>
            <template v-if="user.is_staff">
              <b-dropdown-item :href="$config.get('adminUrl')" class="app-header__nav-right__user__admin">
                {{ $t('appHeader.admin') }}
              </b-dropdown-item>
              <b-dropdown-divider />
            </template>
            <b-dropdown-item :href="$config.get('logoutUrl')" class="app-header__nav-right__user__logout">
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

    & /deep/ .nav-item,
    & /deep/ .nav-item .nav-link,
    & /deep/ .nav-item .dropdown-toggle {
      display: flex;
      align-items: center;
    }
  }
</style>
