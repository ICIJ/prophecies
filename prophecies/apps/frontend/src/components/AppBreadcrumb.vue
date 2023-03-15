<script>
export default {
  name: 'AppBreadcrumb'
}
</script>

<template>
  <ul class="app-breadcrumb list-inline my-3 mx-5">
    <li class="list-inline-item app-breadcrumb__item app-breadcrumb__item--dashboard">
      <router-link :to="{ name: 'dashboard' }">
        <home-icon size="1.5x" />
      </router-link>
    </li>
    <slot name="items">
      <li class="list-inline-item app-breadcrumb__item">
        <slot />
      </li>
    </slot>
  </ul>
</template>

<style lang="scss" scoped>
  .app-breadcrumb {
    display: inline-flex;
    align-items: center;

    &__item--dashboard svg {
      transform: translateY(-0.2em);
    }

    &__item.list-inline-item {
      font-size: $font-size-lg;
      padding-right: $spacer-sm;
      margin-right: 0;
      display: inline-flex;
      align-items: center;
      font-weight: 600;

      &:not(:last-of-type):after {
        content: "";
        background: center right no-repeat;
        background-size: contain;
        background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNyIgaGVpZ2h0PSIxMiIgdmlld0JveD0iMCAwIDcgMTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPHBhdGggZD0iTTEgMTAuNzIwOUw2IDUuODYwNDRMMSAxIiBzdHJva2U9IiMyMzVCNTkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
        margin-left: $spacer-sm;
        display: block;
        height: 1em;
        width: 0.5em;
      }
    }
  }
</style>
