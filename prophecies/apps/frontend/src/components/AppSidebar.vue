<script>
import AppBrand from '@/components/AppBrand'
import AppVersion from '@/components/AppVersion'
import ShortkeyBadge from '@/components/ShortkeyBadge'

export default {
  name: 'AppSidebar',
  components: {
    AppBrand,
    AppVersion,
    ShortkeyBadge
  }
}
</script>

<template>
  <div class="app-sidebar d-flex flex-column">
    <app-brand class="app-sidebar__brand"/>
    <div class="app-sidebar__container flex-grow-1">
      <b-nav vertical>
        <slot name="items">
          <b-nav-item :to="{ name: 'dashboard' }" exact>
            <grid-icon class="mr-3"/>
            {{$t('appSidebar.dashboard')}}
          </b-nav-item>
          <b-nav-item :to="{ name: 'stats-list' }">
            <inbox-icon class="mr-3"/>
            {{$t('appSidebar.myTasks')}}
            <shortkey-badge :value="['Ctrl', 'm']" class="ml-2"/>
          </b-nav-item>
          <b-nav-item :to="{ name: 'shortcut-list' }">
            <command-icon class="mr-3"/>
            {{$t('appSidebar.shortcuts')}}
            <shortkey-badge :value="['Ctrl', 'k']" class="ml-2"/>
          </b-nav-item>
          <b-nav-item :to="{ name: 'tip-list' }">
            <smile-icon class="mr-3"/>
            {{$t('appSidebar.tips')}}
            <shortkey-badge :value="['Ctrl', 'Shift', 't']" class="ml-2"/>
          </b-nav-item>
          <b-nav-item :to="{ name: 'history' }">
            <clock-icon class="mr-3"/>
            {{$t('appSidebar.history')}}
            <shortkey-badge :value="['Ctrl', 'Shift', 'h']" class="ml-2"/>
          </b-nav-item>
          <b-nav-item :href="$config.get('adminUrl')">
            <trello-icon class="mr-3"/>
            {{$t('appSidebar.admin')}}
          </b-nav-item>
        </slot>
      </b-nav>
    </div>
    <div class="app-sidebar__footer">
      <app-version class="px-4 py-3 d-block text-muted"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.app-sidebar {
  max-width: 260px;
  min-height: 100vh;
  font-size: $font-size-lg;

  &__container {

    & ::v-deep .nav-item > * {
      display: flex;
      align-items: center;
      padding: $spacer-lg;
      white-space: nowrap;

      &.router-link-active {
        font-weight: 800;
      }
    }
  }
}
</style>
