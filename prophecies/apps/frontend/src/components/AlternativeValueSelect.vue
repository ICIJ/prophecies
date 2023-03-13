<script>
import {find, get, uniqueId} from 'lodash'
import Multiselect from 'vue-multiselect'
import ChoiceGroup from '@/models/ChoiceGroup'

export default {
  name: 'AlternativeValueSelect',
  model: {
    prop: 'alternativeValue',
    event: 'update:alternativeValue'
  },
  props: {
    alternativeValue: {
      type: String,
      default: null
    },
    choiceGroupId: {
      type: [String, Number]
    }
  },
  components: {
    Multiselect
  },
  methods: {
    selectAlternativeValue({value = null}) {
      /**
       * Fired when the user selected an alternative value
       * @event update:alternativeValue
       * @param The alternative value
       */
      this.$emit('update:alternativeValue', value)
    },
    findAlternativeValue(predicate = {}) {
      return find(this.alternativeValues, predicate)
    },
    toSerializableOption(value) {
      const id = uniqueId('arbitrary-')
      const name = value
      return {id, name, value}
    }
  },
  computed: {
    alternativeValueOption: {
      get() {
        if (this.isCanonical) {
          return this.findAlternativeValue({value: this.alternativeValue})
        } else if (this.alternativeValue !== null) {
          return this.toSerializableOption(this.alternativeValue)
        }
        return null
      },
      set(option = null) {
        this.selectAlternativeValue(option === null ? {value: null} : option)
      }
    },
    alternativeValues() {
      return get(this, 'choiceGroup.alternativeValues', [])
    },
    isCanonical() {
      const value = this.alternativeValue
      return !!this.findAlternativeValue({value})
    },
    choiceGroup() {
      return ChoiceGroup
        .query()
        .with('alternativeValues')
        .find(this.choiceGroupId)
    }
  }
}
</script>

<template>
  <div class="alternative-value-select pb-3">
    <multiselect
      class="multiselect--md"
      :placeholder="$t('alternativeValueSelect.selectTheCorrectValue')"
      v-model="alternativeValueOption"
      label="name"
      track-by="value"
      taggable
      :tag-placeholder="$t('alternativeValueSelect.useThisExactValue')"
      tag-position="bottom"
      @tag="selectAlternativeValue({ value: $event })"
      :options="alternativeValues"/>
  </div>
</template>
