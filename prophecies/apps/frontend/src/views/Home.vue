<template>
  <div class="home container my-4">
    <div class="card card-body">
      <div class="d-flex align-items-start">
        <brand :background="primaryColor" color="#FFFF" />
        <div class="pl-4">
          <h1>Heading 1</h1>
          <h2>Heading 2</h2>
          <h3>Heading 3</h3>
          <h4>Heading 4</h4>
          <p class="lead">
            Lead text, usualy to display the leading text of a page.
          </p>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
          <p>
            <b-btn variant="primary" class="mr-2">
              Primary
            </b-btn>
            <b-btn variant="secondary" class="mr-2">
              Secondary
            </b-btn>
            <b-btn variant="tertiary" class="mr-2">
              Tertiary
            </b-btn>
            <b-btn variant="danger" class="mr-2">
              Danger
            </b-btn>
            <b-btn variant="warning" class="mr-2">
              Warning
            </b-btn>
            <b-btn variant="info" class="mr-2">
              Info
            </b-btn>
            <b-btn variant="dark" class="mr-2">
              Dark
            </b-btn>
            <b-btn variant="light" class="mr-2">
              Light
            </b-btn>
            <b-btn variant="link" class="mr-2">
              Link
            </b-btn>
          </p>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
          <b-alert dismissible show variant="info">An "info" alert</b-alert>
          <b-alert dismissible show variant="danger">An "danger" alert</b-alert>
          <b-alert dismissible show variant="warning">An "warning" alert</b-alert>
          <b-alert dismissible show variant="success">An "success" alert</b-alert>
        </div>
      </div>
      <hr />
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
