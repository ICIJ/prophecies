<script>
import AppVersion from '@/components/AppVersion'
import ShortkeyBadge from '@/components/ShortkeyBadge'

export default {
  name: 'AppSidebar',
  components: {
    AppVersion,
    ShortkeyBadge
  }
}
</script>

<template>
  <div class="app-sidebar d-flex flex-column">
    <router-link class="app-sidebar__brand" :to="{ name: 'dashboard' }">
      <h1 class="app-sidebar__brand__app-name mb-0 font-weight-bold">
        {{ $config.get('appName') }}
      </h1>
      <div class="app-sidebar__brand__org-name">
        {{ $config.get('orgName') }}
      </div>
    </router-link>
    <div class="app-sidebar__container flex-grow-1">
      <b-nav vertical>
        <b-nav-item :to="{ name: 'dashboard' }">
          <grid-icon class="mr-2" />
          Dashboard
        </b-nav-item>
        <b-nav-item>
          <smile-icon class="mr-2" />
          Tips
          <shortkey-badge :value="['meta', 't']" class="ml-2" />
        </b-nav-item>
        <b-nav-item>
          <command-icon class="mr-2" />
          Shortcuts
          <shortkey-badge :value="['meta', 'k']" class="ml-2" />
        </b-nav-item>
        <b-nav-item>
          <clock-icon class="mr-2" />
          History
          <shortkey-badge :value="['meta', 'h']" class="ml-2" />
        </b-nav-item>
        <b-nav-item :href="$config.get('adminUrl')">
          <trello-icon class="mr-2" />
          Admin
        </b-nav-item>
      </b-nav>
    </div>
    <div class="app-sidebar__footer">
      <app-version class="px-4 py-3 d-block text-center text-muted" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .app-sidebar {
    max-width: 260px;
    min-height: 100vh;
    font-size: $font-size-lg;

    &__brand {
      display: block;
      padding: $spacer $spacer-lg 60px;
      color: $primary;

      &:hover {
        text-decoration: none;
      }

      &__org-name {
        font-weight: 300;
      }
    }

    &__container {

      & /deep/ .nav-item > * {
        display: flex;
        align-items: center;
        padding: $spacer-lg;

        &.router-link-active {
          font-weight: 800;
        }
      }
    }
  }
</style>
