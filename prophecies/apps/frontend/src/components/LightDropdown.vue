<script>
import { directive as onClickaway } from 'vue-clickaway'
import { find } from 'lodash'

export default {
  name: 'LightDropdown',
  directives: {
    onClickaway
  },
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
  data() {
    return {
      show: false
    }
  },
  computed: {
    selectedId_: {
      get() {
        return this.selectedId
      },
      set(value) {
        this.$emit('update:selectedId', value)
      }
    },
    selectedItem() {
      return find(this.items, { id: this.selectedId_ })
    }
  },
  methods: {
    toggle() {
      this.show = !this.show
    },
    close() {
      this.show = false
    },
    select(e) {
      this.selectedId_ = e.target.dataset.itemid
    },
    isActive(itemId) {
      return this.selectedId_ === itemId
    }
  }
}
</script>

<template>
  <div class="light-dropdown dropdown" :class="{ show: show }">
    <span
      id="dropdownMenuButton"
      v-on-clickaway="close"
      class="light-dropdown__selected text-primary dropdown-toggle font-weight-bold"
      :class="btnClassList"
      type="button"
      aria-haspopup="true"
      :aria-expanded="!show"
      @click="toggle"
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
        class="dropdown-item"
        :class="{ active: isActive(item.id) }"
        :data-itemid="item.id"
        @click="select"
      >
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>
