<script>
import { find, get, uniqueId } from 'lodash'
import { toVariant } from '@/utils/variant'
import Choice from '@/models/Choice'
import ChoiceGroup from '@/models/ChoiceGroup'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewChoiceForm',
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    }
  },
  filters: {
    toVariant
  },
  data () {
    return {
      alternativeValue: ''
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
      return choice.id === this.taskRecordReview.choice_id
    },
    choiceClassList (choice) {
      return {
        'task-record-review-choice-form__choices__item--selected': this.choiceIsSelected(choice)
      }
    },
    async selectChoice (choice) {
      if (choice.require_alternative_value && !this.alternativeValue) {
        return this.$refs.alternativeValueInput.focus()
      }
      const alternativeValue = choice.require_alternative_value ? this.alternativeValue : ''
      const data = { alternative_value: alternativeValue, choice }
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
    setInitialValues () {
      this.alternativeValue = get(this, 'taskRecordReview.alternative_value', '')
    }
  },
  computed: {
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('choice')
        .with('task_record')
        .with('task_record.task')
        .find(this.taskRecordReviewId)
    },
    alternativeValueChoice () {
      const choices = get(this, 'choiceGroup.choices', [])
      return find(choices, { require_alternative_value: true })
    },
    alternativeValues () {
      return get(this, 'choiceGroup.alternative_values', [])
    },
    choiceGroup () {
      return ChoiceGroup
        .query()
        .with('choices')
        .with('alternative_values')
        .find(this.taskRecordReview.task_record.task.choice_group_id)
    },
    classList () {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue
      }
    },
    hasAlternativeValue () {
      return !!get(this, 'taskRecordReview.alternative_value', '')
    },
    hasChoice () {
      return !!get(this, 'taskRecordReview.choice', false)
    }
  }
}
</script>

<template>
  <fieldset class="task-record-review-choice-form py-1" :class="classList">
    <ul class="task-record-review-choice-form__choices list-unstyled row no-gutters m-0">
      <li v-for="choice in choiceGroup.choices" :key="choice.id" class="col px-2 pb-3">
        <b-btn @click="selectChoice(choice)"
               block
               class="task-record-review-choice-form__choices__item text-nowrap"
               :class="choiceClassList(choice)"
               :variant="choice.value | toVariant">
          {{ choice.name }}
        </b-btn>
      </li>
    </ul>
    <div class="px-2 task-record-review-choice-form__alternative-value" v-if="alternativeValueChoice">
      <b-form-select v-model="alternativeValue" @change="selectAlternativeValue" class="mb-3" ref="alternativeValueInput">
        <b-form-select-option value="">
          Select the correct value
        </b-form-select-option>
        <b-form-select-option v-for="{ id, value, name } in alternativeValues" :value="value" :key="id">
          {{ name }}
        </b-form-select-option>
      </b-form-select>
    </div>
  </fieldset>
</template>

<style lang="scss" scoped>
  .task-record-review-choice-form {

    &__choices {

      &__item {
        font-weight: normal;
      }

      .task-record-review-choice-form--has-choice &__item {
        opacity: 0.25;
      }

      .task-record-review-choice-form--has-choice & &__item--selected {
        opacity: 1;
        font-weight: bold;
      }
    }

    &--has-choice:not(&--has-alternative-value) &__alternative-value select:not(:focus) {
      opacity: 0.25;
    }
  }
</style>
