<script>
import { find, get, uniqueId } from 'lodash'
import Multiselect from 'vue-multiselect'
import { toVariant } from '@/utils/variant'
import Choice from '@/models/Choice'
import ChoiceGroup from '@/models/ChoiceGroup'
import TaskRecordReview from '@/models/TaskRecordReview'
import ShortkeyBadge from '@/components/ShortkeyBadge'

export default {
  name: 'TaskRecordReviewChoiceForm',
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    activateShortkeys: {
      type: Boolean
    }
  },
  components: {
    Multiselect,
    ShortkeyBadge
  },
  filters: {
    toVariant
  },
  data () {
    return {
      alternativeValue: null
    }
  },
  created () {
    this.setInitialValues()
  },
  watch: {
    taskRecordReview () {
      this.setInitialValues()
    }
  },
  methods: {
    choiceIsSelected (choice) {
      return choice.id === this.taskRecordReview.choiceId
    },
    choiceClassList (choice) {
      return {
        'task-record-review-choice-form__choices__item--selected': this.choiceIsSelected(choice)
      }
    },
    choiceShortkeys (choice) {
      if (!this.activateShortkeys || !choice.shortkeys) {
        return null
      }
      return choice.shortkeys.split(',')
    },
    focusOnAlternativeValueInput () {
      const input = this.$refs.alternativeValueInput.$el.querySelector('input')
      if (input) {        
        input.focus()
      }
    },
    async selectChoice (choice) {
      if (choice.requireAlternativeValue && !this.alternativeValue) {
        return this.focusOnAlternativeValueInput()
      }
      const alternativeValue = choice.requireAlternativeValue ? this.alternativeValue.value : null
      const data = { alternativeValue, choice }
      /**
       * Fired when the form is submitted
       * @event submit
       * @param The changed attributes and relationships
       */
      this.$emit('submit', data)
    },
    async selectAlternativeValue () {
      await this.selectChoice(this.alternativeValueChoice)
    },
    async addArbitraryAlternativeValue (value) {
      this.alternativeValue = this.toSerializableOption(value)
      await this.selectAlternativeValue()
    },
    findAlternativeValue (predicate) {
      return find(this.alternativeValues, predicate)
    },
    setInitialValues () {
      const value = get(this, 'taskRecordReview.alternativeValue', null)
      if (value) {
        const alternativeValue = this.findAlternativeValue({ value })
        this.alternativeValue = alternativeValue || this.toSerializableOption(value)
      }
    },
    toSerializableOption (value) {
      const id = uniqueId('arbitrary-')
      const name = value
      return { id, name, value }
    }
  },
  computed: {
    taskRecord () {
      return this.taskRecordReview.taskRecord
    },
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('choice')
        .with('taskRecord')
        .with('taskRecord.task')
        .find(this.taskRecordReviewId)
    },
    alternativeValueChoice () {
      const choices = get(this, 'choiceGroup.choices', [])
      return find(choices, { requireAlternativeValue: true })
    },
    alternativeValues () {
      return get(this, 'choiceGroup.alternativeValues', [])
    },
    choiceGroup () {
      return ChoiceGroup
        .query()
        .with('choices')
        .with('alternativeValues')
        .find(this.taskRecordReview.taskRecord.task.choiceGroupId)
    },
    classList () {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue,
        'task-record-review-choice-form--is-locked': this.isLocked
      }
    },
    hasAlternativeValue () {
      return get(this, 'taskRecordReview.alternativeValue', false)
    },
    hasChoice () {
      return !!get(this, 'taskRecordReview.choiceId', false)
    },
    isLocked () {
      return this.taskRecord.locked
    }
  }
}
</script>

<template>
  <fieldset class="task-record-review-choice-form py-1" :class="classList" :disabled="isLocked">
    <ul class="task-record-review-choice-form__choices list-unstyled row">
      <li v-for="choice in choiceGroup.choices"
          class="col pb-3 task-record-review-choice-form__choices__item"
          :class="choiceClassList(choice)"
          :key="choice.id">
        <b-btn @click="selectChoice(choice)"
               @shortkey="selectChoice(choice)"
               v-shortkey="choiceShortkeys(choice)"
               block
               class="task-record-review-choice-form__choices__item__button text-nowrap"
               :variant="choice.value | toVariant">
          {{ choice.name }}
          <template v-if="choiceShortkeys(choice)">
            <shortkey-badge class="ml-1" :value="choice.shortkeys" />
          </template>
        </b-btn>
      </li>
    </ul>
    <div class="task-record-review-choice-form__alternative-value" v-if="alternativeValueChoice">
      <multiselect ref="alternativeValueInput"
         placeholder="Select the correct value"
         v-model="alternativeValue"
         label="name"
         track-by="value"
         taggable
         tag-placeholder="Use this exact value"
         tag-position="bottom"
         @input="selectAlternativeValue()"
         @tag="addArbitraryAlternativeValue"
         :options="alternativeValues" />
    </div>
  </fieldset>
</template>

<style lang="scss" scoped>
  .task-record-review-choice-form {

    &__choices {
      margin: 0 -$spacer-xs;
      margin-bottom: 0;

      &__item {
        font-weight: normal;
        padding: 0 $spacer-xs;
        transition: $transition-fade;

        &__button /deep/ .shortkey-badge {
          color: inherit;
        }
      }

      .task-record-review-choice-form--has-choice:not(:hover) &__item {
        opacity: 0.25;
      }

      .task-record-review-choice-form--has-choice & &__item--selected {
        opacity: 1;
        font-weight: bold;
      }
    }

    &__alternative-value .multiselect {
      transition: $transition-fade;
    }

    &--has-choice:not(:hover):not(&--has-alternative-value) &__alternative-value .multiselect:not(.multiselect--active) {
      opacity: 0.25;
    }
  }
</style>
