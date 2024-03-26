<script>
import { textContrast } from '@/utils/color'
export default {
  name: 'TaskProgress',
  filters: {
    taskProgressStyle(color) {
      return color ? `--progress-fg: ${color};--text-color:${textContrast(color)}` : ''
    },
    round(value) {
      return Math.round(value)
    }
  },
  props: {
    progress: {
      type: Number
    },
    color: {
      type: String
    }
  }
}
</script>

<template>
  <span class="task-progress text-center rounded font-weight-bold" :style="color | taskProgressStyle">
    {{ progress }}%
  </span>
</template>

<style lang="scss" scoped>
.task-progress {
  width: 50px;
  background: var(--progress-fg, $primary) !important;
  color: var(--text-color, $body-bg) !important;
}
</style>
