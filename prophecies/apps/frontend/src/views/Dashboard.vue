<template>
  <div class="dashboard d-flex">
    <app-sidebar class="w-100" />
    <div class="dashboard__container flex-grow-1">
      <app-header />
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'

export default {
  name: 'Dashboard',
  components: {
    AppHeader,
    AppSidebar
  }
}
</script>
