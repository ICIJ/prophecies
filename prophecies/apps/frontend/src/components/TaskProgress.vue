<script>
import { textContrast } from '@/utils/color'
export default {
  name: 'TaskProgress',
  props: {
    progress: {
      type: Number
    },
    color: {
      type: String
    }
  },
  filters: {
    taskProgressStyle (color) {
      if (!color) {
        return ''
      }
      const textColor = textContrast(color)
      return `--progress-fg: ${color};--text-color:${textColor}`
    },
    round (value) {
      return Math.round(value)
    }
  }
}
</script>

<template>
  <span
    class="
      task-progress
      text-center
      rounded
      font-weight-bold
    "
    :style="color | taskProgressStyle"
  >
    {{progress}}%
  </span>
</template>

<style lang="scss" scoped>
.task-progress {
      width: 50px;
      background: var(--progress-fg, $primary) !important;
      color: var(--text-color, $body-bg) !important;
}
</style>
