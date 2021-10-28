<template>
  <div class="stats-list d-flex align-items-start">
   <app-sidebar class="w-100 sticky-top" />
    <div class="stats-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
          hi!
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar'
export default {
  name: 'StatsList',
  components: {
    AppHeader,
    AppSidebar
  },
  props: {

  },
  data () {
    return {

    }
  },
  computed: {

  }
}
</script>

<style lang="scss" scoped>
</style>
