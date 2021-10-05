<template>
  <div class="shortcut-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="shortcut-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid pl-4 pt-5">
        <shortcut-list-card :width="width" />
      </div>
    </div>
  </div>
</template>

<script>
import { uniqueId, flatMap } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import ShortcutListCard from '@/components/ShortcutListCard'

export default {
  name: 'ShortcutList',
  components: {
    AppSidebar,
    AppHeader,
    ShortcutListCard
  },
  data () {
    return {
      width: 'w-75'
    }
  }
}

</script>

<style lang="scss" scoped>
</style>
