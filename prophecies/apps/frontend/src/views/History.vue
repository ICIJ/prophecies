<script>
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import HistoryList from '@/components/HistoryList'

export default {
  name: 'History',
  components: {
    AppSidebar,
    AppHeader,
    HistoryList
  }
}
</script>

<template>
  <div class="history d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="history__container flex-grow-1">
      <app-header reduced />
      <history-list >
        <template v-slot:title>
        <h1 class="font-weight-bold mb-5 history__title">What happened <span class="history__title--lately">lately</span></h1>
        </template>
      </history-list>
    </div>
  </div>
</template>

<style lang="scss" scoped>
 .history {
    &__title{
      color:$primary;
      &--lately{
        color:$danger;
      }
    }
 }
</style>
