<script>
import { castArray, flatten, trim } from 'lodash'
import { toUpperCaseForSingleChar, metaKeyDisplay } from '@/utils/keys'

export default {
  name: 'ShortkeyBadge',
  props: {
    value: {
      type: [Array, String],
      default: ''
    }
  },
  computed: {
    keys () {
      const keys = flatten(castArray(this.value).map(key => key.split('+')))
      return keys
        .map(trim)
        .map(toUpperCaseForSingleChar)
        .map(metaKeyDisplay)
    },
    keysAsString () {
      return this.keys.join(' + ')
    }
  }
}
</script>

<template>
  <span class="shortkey-badge badge font-weight-normal" v-show="keys.length">
    {{ keysAsString }}
  </span>
</template>

<style lang="scss" scoped>
  .shortkey-badge {
    color: $secondary;
    border: 1px solid currentColor;
    background: transparent;
    min-width: calc(1em + #{$badge-padding-x * 2});
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
</style>
