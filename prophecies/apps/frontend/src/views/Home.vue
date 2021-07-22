<template>
  <div class="home container my-4">
    <div class="card card-body">
      <div class="d-flex align-items-center">
        <brand :background="primaryColor" color="#FFFF" />
        <div class="pl-4">
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </div>
      <b-btn :href="logoutUrl" class="ml-auto">
        Logout
      </b-btn>
    </div>
  </div>
</template>

<script>
import settings from '@/settings'

export default {
  name: 'Home',
  computed: {
    logoutUrl () {
      return settings.logoutUrl
    },
    primaryColor () {
      const style = getComputedStyle(document.body)
      return style.getPropertyValue(`--primary`) || '#A10207'
    }
  }
}
</script>
