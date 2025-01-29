<script>
import { some, get } from 'lodash'

import Choice from '@/models/Choice'
import ChoiceGroup from '@/models/ChoiceGroup'
import AlternativeValueSelect from '@/components/AlternativeValueSelect'
import ChoiceGroupButtons from '@/components/ChoiceGroupButtons'
import TaskRecordReview from '@/models/TaskRecordReview'
import { TaskStatusEnum } from '@/models/Task'

export default {
  name: 'TaskRecordReviewChoiceForm',
  components: {
    AlternativeValueSelect,
    ChoiceGroupButtons
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    activateShortkeys: {
      type: Boolean
    },
    alternativeValueInputSelector: {
      type: String,
      default: '.alternative-value-select input'
    }
  },
  data() {
    return {
      alternativeValueChoice: null
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
        this.alternativeValueChoice = Choice.find(choiceId)
        return this.selectChoice(this.alternativeValueChoice, this.alternativeValue)
      }
    },
    choiceGroupId() {
      return get(this, 'choiceGroup.id', null)
    },
    choiceGroup() {
      return ChoiceGroup.query().with('choices').find(this.taskRecord.task.choiceGroupId)
    },
    taskRecord() {
      return get(this, 'taskRecordReview.taskRecord')
    },
    taskRecordReview() {
      return TaskRecordReview.query()
        .with('choice')
        .with('taskRecord')
        .with('taskRecord.task')
        .find(this.taskRecordReviewId)
    },
    classList() {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue,
        'task-record-review-choice-form--is-locked': this.isLocked
      }
    },
    hasAlternativeValue() {
      return get(this, 'taskRecordReview.alternativeValue', false)
    },
    hasChoice() {
      return this.choiceId !== null
    },
    canSelectAlternativeValue() {
      const choices = get(this, 'choiceGroup.choices', [])
      return !!some(choices, { requireAlternativeValue: true })
    },
    disable() {
      return this.isLocked || !this.taskRecordReview.editable
    },
    isLocked() {
      return this.taskRecord.locked || this.taskIsNotOpen
    },
    taskIsNotOpen() {
      return this.taskRecord.task.status !== TaskStatusEnum.OPEN
    }
  },
  mounted() {
    this.alternativeValueChoice = this.taskRecordReview.choice
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
  <fieldset class="task-record-review-choice-form py-1" :class="classList" :disabled="disable">
    <choice-group-buttons
      v-model="choiceId"
      class="task-record-review-choice-form__choices"
      :activate-shortkeys="activateShortkeys"
      :choice-group-id="choiceGroupId"
    />
    <alternative-value-select
      v-if="canSelectAlternativeValue"
      ref="alternativeValueInput"
      v-model="alternativeValue"
      class="task-record-review-choice-form__alternative-value"
      :choice-group-id="choiceGroupId"
    />
  </fieldset>
</template>

<style lang="scss" scoped>
.task-record-review-choice-form {
  &__alternative-value ::v-deep .multiselect {
    transition: $transition-fade;
  }

  &--has-choice:not(:hover):not(&--has-alternative-value)
    &__alternative-value
    ::v-deep
    .multiselect:not(.multiselect--active) {
    opacity: 0.25;
  }
}
</style>
