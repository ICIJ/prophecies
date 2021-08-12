<script>
import { find, get, uniqueId } from 'lodash'
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
      return choice.id === this.taskRecordReview.choice_id
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
    async selectChoice (choice) {
      if (choice.requireAlternativeValue && !this.alternativeValue) {
        return this.$refs.alternativeValueInput.focus()
      }
      const alternativeValue = choice.requireAlternativeValue ? this.alternativeValue : null
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
    setInitialValues () {
      this.alternativeValue = get(this, 'taskRecordReview.alternativeValue', null) || null
    }
  },
  computed: {
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
        .find(this.taskRecordReview.taskRecord.task.choiceGroup_id)
    },
    classList () {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue
      }
    },
    hasAlternativeValue () {
      return get(this, 'taskRecordReview.alternativeValue', false)
    },
    hasChoice () {
      return !!get(this, 'taskRecordReview.choice_id', false)
    }
  }
}
</script>

<template>
  <fieldset class="task-record-review-choice-form py-1" :class="classList">
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
      <b-form-select v-model="alternativeValue" @change="selectAlternativeValue"  ref="alternativeValueInput">
        <b-form-select-option :value="null">
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

    &__alternative-value select {
      transition: $transition-fade;
    }

    &--has-choice:not(:hover):not(&--has-alternative-value) &__alternative-value select:not(:focus) {
      opacity: 0.25;
    }
  }
</style>
