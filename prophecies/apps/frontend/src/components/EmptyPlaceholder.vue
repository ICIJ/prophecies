<script>
import { isObject, find } from 'lodash'
import * as icons from '@/utils/icons'

export default {
  name: 'EmptyPlaceholder',
  props: {
    icon: {
      type: [String, Object],
      required: false
    },
    title: {
      type: String
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
  <div
    class="
      empty-placeholder
      text-center text-secondary text-small
    "
  >
    <div v-if="icon && iconComponent" class="text-center p-3 text-secondary">
        <component :is="iconComponent" class="empty-placeholder__icon mx-auto" size="3x" ></component>
    </div>
    <slot>
      <p>
        {{ title }}
      </p>
    </slot>
  </div>
</template>
<style lang="scss" scoped>
  .empty-placeholder{

    &__icon {
      margin-top: $spacer-xs;
      max-width: 30px;
      min-width: 30px;
    }

  }
</style>
