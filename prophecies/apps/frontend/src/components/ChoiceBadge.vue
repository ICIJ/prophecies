<script>
import { uniqueId } from 'lodash'
import { textContrast } from '@/utils/color'

export default {
  name: 'ChoiceBadge',
  props: {
    name: {
      type: String
    },
    value: {
      type: String
    },
    color: {
      type: String
    }
  },
  filters: {
    taskProgressStyle (color) {
      return color ? `--progress-fg: ${color};--text-color:${textContrast(color)}` : ''
    },
    firstLetter (str) {
      return String(str).slice(0, 1)
    },
    skipFirstLetter (str) {
      return String(str).slice(1)
    }
  },
  data () {
    return {
      id: null
    }
  },
  created () {
    this.id = uniqueId('choice-tooltip-')
  }

}
</script>

<template>
  <span :style="color | taskProgressStyle">
    <b-badge class="choice__badge mr-3 p-1" :title="name" :id="id">
      {{ name | firstLetter }}<span class="sr-only">{{ name | skipFirstLetter }}</span>
      <b-tooltip :target="id" triggers="hover" placement="right" >
         <div class="choice__tooltip d-flex align-items-center">
            <span class="py-1 px-2 font-weight-bold ">{{name}}</span><slot name="afterTooltip"/>
         </div>
      </b-tooltip>
    </b-badge>
  </span>
</template>

<style lang="scss">

.choice__badge {

  width: 1.6em;
  height: 1.6em;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  background: var(--progress-fg, $primary) !important;
  color: var(--text-color, $body-bg) !important;

}

</style>
