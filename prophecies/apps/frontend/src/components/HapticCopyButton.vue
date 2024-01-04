<script>
export default {
  name: 'HapticCopyButton',
  props: {
    text: {
      type: String,
      default: ''
    }
  }
}
</script>

<template>
  <haptic-copy
    :text="text"
    class="haptic-copy-button font-weight-bold"
    tooltip-placement="right"
    v-b-tooltip.hover.right="'Click to copy'">
    <template v-if="$slots.default">
      <slot />
    </template>
    <template v-else>
      {{ text }}
    </template>
    <span class="haptic-copy-button__clipboard ml-1">
      <clipboard-icon />
    </span>
  </haptic-copy>
</template>

<style lang="scss" scoped>
.haptic-copy-button {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: $spacer-xs $spacer;

  &:hover {
    background: $primary-10;
  }

  &__clipboard {
    min-width: 1.2rem;
    align-self: center;
    color: $tertiary;
    opacity: 0;
    transition: $btn-transition, opacity .15s;

    .feather {
      height: 1.5em;
    }
  }

  &:focus &__clipboard,
  &:active &__clipboard,
  &:hover &__clipboard {
    opacity: 1;
  }
}
</style>
