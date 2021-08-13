<script>
  import { findIndex } from 'lodash'

  export default {
    name: 'MultiselectButtons',
    model: {
      prop: 'value',
      event: 'update'
    },
    props: {
      value: {
        type: Array,
        default: () => ([])
      },
      options: {
        type: Array,
        default: () => ([])
      },
      label: {
        type: String,
        default: 'name'
      },
      trackBy: {
        type: String,
        default: 'name'
      }
    },
    computed: {
      noValues () {
        return !this.value.length
      }
    },
    methods: {
      findOptionIndex (option = null) {
        if (option === null) {
          return -1
        }
        const tracked = option[this.trackBy]
        return findIndex(this.value, { [this.trackBy]: tracked })
      },
      isOptionSelected (option = null) {
        return (option === null && this.noValues) || this.findOptionIndex(option) > -1
      },
      optionVariant (option = null) {
        return this.isOptionSelected(option) ? 'primary' : 'outline-primary'
      },
      removeOptions () {
        return this.$emit('update', [])
      },
      toggleOption (option) {
        const tracked = option[this.trackBy]
        const index = findIndex(this.value, { [this.trackBy]: tracked })
        if (index === -1) {
          return this.$emit('update', [...this.value, option])
        }
        return this.$emit('update', this.value.slice(index, 1))
      }
    }
  }
</script>

<template>
  <div class="multiselect-buttons">
    <b-btn :variant="optionVariant()" class="multiselect-buttons__item" @click="removeOptions()">
      all
    </b-btn>
    <span v-for="option in options" :key="option[trackBy]">
      <b-btn :variant="optionVariant(option)" class="multiselect-buttons__item mr-3" @click="toggleOption(option)">
        {{ option[label] }}
      </b-btn>
    </span>
  </div>
</template>

<style lang="scss" scoped>
  .multiselect-buttons {
    &__item.btn-outline-primary {
      border-color: $border;
    }

    &__item.btn-primary {
      font-weight: bold;
    }
  }
</style>
