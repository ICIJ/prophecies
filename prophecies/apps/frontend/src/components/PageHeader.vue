<script>
import { isObject, find } from 'lodash'
import * as icons from '@/utils/icons'

export default {
  name: 'PageHeader',
  props: {
    title: { 
      type: String
    },
    icon: {
      type: [String, Object]
    }
  },
  computed: {
    iconComponent () {
      if (isObject(this.icon)) {
        return this.icon
      }
      return this.matchingIconComponent
    },
    matchingIconComponent () {
      return find(icons, ({ name }) => name.startsWith(this.icon))
    }
  }
}
</script>

<template>
  <header class="page-header text-primary">
    <conponent :is="iconComponent" class="page-header__icon" size="2x" />
    <h1 class="page-header__title mb-0 font-weight-bold">
      <slot>{{ title }}</slot>
    </h1>
  </header>
</template>

<style lang="scss" scoped>
  .page-header {
    display:flex;

    &__icon { 
      margin-top: $spacer-xs;
      margin-right: $spacer-sm;
      max-width: 30px;
      min-width: 30px;
    }

    &__title {
      padding-bottom: $spacer-xs;
      border-bottom: 7px solid $warning;   
    }
  }
</style>