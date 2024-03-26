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
    variant: {
      type: String,
      default: 'light'
    },
    waiterClass: {
      type: [String, Array, Object],
      default: () => ['mx-auto', 'my-1', 'd-block']
    }
  }
}
</script>

<template>
  <v-wait :for="loader" :transition="transition" :mode="mode" :duration="duration">
    <b-spinner slot="waiting" :small="small" :variant="variant" :class="waiterClass" />
    <slot />
  </v-wait>
</template>

<style scoped>
.spinner-border {
  animation-duration: 1s;
}
</style>
