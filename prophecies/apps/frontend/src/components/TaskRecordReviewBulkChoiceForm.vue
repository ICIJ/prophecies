<script>
import { find, get } from 'lodash'

import Choice from '@/models/Choice'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import AlternativeValueSelect from '@/components/AlternativeValueSelect'
import ChoiceGroupButtons from '@/components/ChoiceGroupButtons'

export default {
  name: 'TaskRecordReviewBulkChoiceForm',
  components: {
    AlternativeValueSelect,
    ChoiceGroupButtons
  },
  props: {
    taskId: {
      type: [String, Number]
    },
    disabled: {
      type: Boolean
    },
    activateShortkeys: {
      type: Boolean
    },
    alternativeValueInputSelector: {
      type: String,
      default: '.alternative-value-select input'
    }
  },
  computed: {
    alternativeValue: {
      get() {
        return get(this, 'taskRecordReview.alternativeValue', null)
      },
      set(alternativeValue) {
        return this.selectChoice(this.alternativeValueChoice, alternativeValue)
      }
    },
    choiceId: {
      get() {
        return get(this, 'taskRecordReview.choiceId', null)
      },
      set(choiceId) {
        const choice = Choice.find(choiceId)
        return this.selectChoice(choice)
      }
    },
    choiceGroupId() {
      return get(this, 'choiceGroup.id', null)
    },
    choiceGroup() {
      return ChoiceGroup.query().with('choices').find(this.task.choiceGroupId)
    },
    task() {
      return Task.find(this.taskId)
    },
    alternativeValueChoice() {
      const choices = get(this, 'choiceGroup.choices', [])
      return find(choices, { requireAlternativeValue: true })
    }
  },
  methods: {
    focusOnAlternativeValueInput() {
      const input = this.$el.querySelector(this.alternativeValueInputSelector)
      if (input) {
        input.focus()
      }
    },
    selectChoice(choice, alternativeValue = null) {
      if (choice.requireAlternativeValue && !alternativeValue) {
        return this.focusOnAlternativeValueInput()
      }
      alternativeValue = choice.requireAlternativeValue ? alternativeValue : null
      /**
       * Fired when the form is submitted
       * @event submit
       * @param The changed attributes and relationships
       */
      this.$emit('submit', { alternativeValue, choice })
    }
  }
}
</script>

<template>
  <fieldset :disabled="disabled" class="task-record-review-bulk-choice-form">
    <choice-group-buttons
      v-model="choiceId"
      class="task-record-review-bulk-choice-form__choices"
      :activate-shortkeys="activateShortkeys"
      :choice-group-id="choiceGroupId"
    />
    <alternative-value-select
      v-if="alternativeValueChoice"
      ref="alternativeValueInput"
      v-model="alternativeValue"
      class="task-record-review-bulk-choice-form__alternative-value"
      small
      :choice-group-id="choiceGroupId"
    />
  </fieldset>
</template>

<style lang="scss" scoped>
.task-record-review-bulk-choice-form {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;

  &__choices,
  &__alternative-value {
    margin-top: 0;
    margin-bottom: 0;
  }

  &__choices {
    margin-right: $spacer-xs;
  }

  &__alternative-value {
    max-width: 400px;
    width: 100%;
  }
}
</style>
