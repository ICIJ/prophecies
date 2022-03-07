<script>
import { directive as onClickaway } from 'vue-clickaway'
import { find } from 'lodash'

export default {
  name: 'LightDropdown',
  props: {
    selectedId: {
      type: String
    },
    items: {
      type: Array
    },
    btnClassList: {
      type: Array,
      default: () => []

    }
  },
  directives: {
    onClickaway
  },
  data () {
    return {
      show: false
    }
  },
  computed: {
    selectedId_: {
      get () {
        return this.selectedId
      },
      set (value) {
        this.$emit('update:selectedId', value)
      }
    },
    selectedItem () {
      const newLocal = find(this.items, { id: this.selectedId_ })
      return newLocal
    }
  },
  methods: {
    toggle () {
      this.show = !this.show
    },
    close () {
      this.show = false
    },
    select (e) {
      this.selectedId_ = e.target.dataset.itemid
    },
    isActive (itemId) {
      return this.selectedId_ === itemId
    }
  }
}
</script>

<template>
  <div
      class="light-dropdown dropdown"
      :class="{ show: show }"
  >
      <span
      class="light-dropdown__selected
      text-primary
      dropdown-toggle
      font-weight-bold"
      :class="btnClassList"
      type="button"
      id="dropdownMenuButton"
      v-on-clickaway="close"
      @click="toggle"
      aria-haspopup="true"
      :aria-expanded="!show"
      >
      {{ selectedItem.name }}
      </span>
      <ul
      class="light-dropdown__options dropdown-menu dropdown-menu-right"
      :class="{ show: show }"
      aria-labelledby="dropdownMenuButton"
      >
      <li
          v-for="item in items"
          :key="item.id"
          @click="select"
          class="dropdown-item"
          :class="{ active: isActive(item.id) }"
          :data-itemid="item.id"
      >
          {{ item.name }}
      </li>
      </ul>
  </div>
</template>
