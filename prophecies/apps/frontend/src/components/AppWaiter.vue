<script>
/**
 * A component that wraps the v-wait component to provide a unique spinner
 * experience between views and components.
 */
export default {
  name: 'AppWaiter',
  props: {
    duration: {
      type: Number,
      default: 400
    },
    mode: {
      type: String,
      default: 'out-in'
    },
    loader: {
      type: String
    },
    small: {
      type: Boolean
    },
    transition: {
      type: String,
      default: 'fade'
    },
    waiterClass: {
      type: [String, Array, Object],
      default: () => (['mx-auto', 'my-1', 'd-block'])
    }
  }
}
</script>

<template>
  <v-wait :for="loader" :transition="transition" :mode="mode" :duration="duration">
    <b-spinner :small="small" variant="light" slot="waiting" :class="waiterClass" />
    <slot />
  </v-wait>
</template>

<style scoped>
  .spinner-border {
    animation-duration: 1.5s;
  }
</style>
