<script>
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import ShortcutListCard from '@/components/ShortcutListCard'

export default {
  name: 'ShortcutList',
  components: {
    AppSidebar,
    AppHeader,
    ShortcutListCard
  }
}

</script>

<template>
  <div class="shortcut-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="shortcut-list__container flex-grow-1">
      <app-header hide-nav />
      <div class="container-fluid pl-4 pt-5">
        <shortcut-list-card hide-title />
      </div>
    </div>
  </div>
</template>
