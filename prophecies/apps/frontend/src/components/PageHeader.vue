<script>

export default {
  name: 'PageHeader',
  props: {
    title: {
      type: String
    }
  }
}
</script>

<template>
  <header class="page-header text-primary">
    <h1 class="page-header__title mb-0 font-weight-bold">
      <slot>{{ title }}</slot>
    </h1>
  </header>
</template>

<style lang="scss" scoped>
  .page-header {
    display:flex;

    &__title {
      padding-bottom: $spacer-xs;
      border-bottom: 7px solid $warning;
    }
  }
</style>
