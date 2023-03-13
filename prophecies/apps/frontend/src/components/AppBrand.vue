<template>
  <router-link class="app-brand" :to="{ name: 'dashboard' }">
    <h1 class="app-brand__app-name mb-0 font-weight-bold">
      <img class="app-brand__app-name__logo" src="@/assets/images/name-and-logo.svg" :alt="$config.get('appName')"/>
    </h1>
    <div class="app-brand__org-name">
      {{ $config.get('orgName') }}
    </div>
  </router-link>
</template>

<style lang="scss" scoped>
.app-brand {
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
</style>
