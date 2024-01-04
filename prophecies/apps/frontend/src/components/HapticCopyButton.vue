<script>
export default {
  name: 'HapticCopyButton',
  props: {
    text: {
      type: String,
      default: ''
    },
    hover: {
      type: Boolean
    }
  }
}
</script>

<template>
  <haptic-copy
    :text="text"
    :class="{ 'haptic-copy-button--hover': hover }"
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
  background: $primary-10;

  &:hover {
    background: $primary-10;
  }

  &__clipboard {
    min-width: 1.2rem;
    align-self: center;
    color: $tertiary;

    .feather {
      height: 1.5em;
    }
  }

  &--hover &__clipboard {
    opacity: 0;
    transition: $btn-transition, opacity .15s;
  }

  &--hover {
    background: transparent;
  }

  &:focus &__clipboard,
  &:active &__clipboard,
  &:hover &__clipboard {
    opacity: 1;
  }
}
</style>
