<script>
import { get, uniqueId } from 'lodash'
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
      alternativeValue: '',
      note: ''
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
    async selectChoiceWithLoader (choice) {
      this.$wait.start(this.updateLoader)
      await this.selectChoice(choice)
      this.$wait.end(this.updateLoader)
    },
    async selectChoice (choice) {
      const data = {  choice, note: this.note, alternative_value: this.alternativeValue }
      await TaskRecordReview.api().selectChoice(this.taskRecordReviewId, data)
      /**
       * @event Fired when the task record review is updated
       */
      this.$emit('update')
    },
    setInitialValues () {
      this.alternativeValue = get(this, 'taskRecordReview.alternative_value', '')
      this.note = get(this, 'taskRecordReview.note', '')
    }
  },
  computed: {
    updateLoader () {
      return uniqueId('update-task-record-review-')
    },
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('choice')
        .with('task_record')
        .with('task_record.task')
        .find(this.taskRecordReviewId)
    },
    choiceGroup () {
      return ChoiceGroup
        .query()
        .with('choices')
        .find(this.taskRecordReview.task_record.task.choice_group_id)
    },
    classList () {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue,
        'task-record-review-choice-form--has-note': this.hasNote
      }
    },
    hasAlternativeValue () {
      return !!get(this, 'taskRecordReview.alternative_value', '')
    },
    hasChoice () {
      return !!get(this, 'taskRecordReview.choice', false)
    },
    hasNote () {
      return !!get(this, 'taskRecordReview.note', '')
    },
    overlayVariant () {
      if (this.taskRecordReview.status === 'DONE') {
        return 'lighter'
      }
      return 'white'
    }
  }
}
</script>

<template>
  <b-overlay :show="$wait.is(updateLoader)" :variant="overlayVariant">
    <b-spinner variant="light" slot="overlay" />
    <fieldset class="task-record-review-choice-form py-1" :class="classList">
      <ul class="task-record-review-choice-form__choices list-unstyled row no-gutters m-0">
        <li v-for="choice in choiceGroup.choices" :key="choice.id" class="col px-2 pb-3">
          <b-btn @click="selectChoiceWithLoader(choice)"
                 block
                 class="task-record-review-choice-form__choices__item"
                 :class="choiceClassList(choice)"
                 :variant="choice.value | toVariant">
            {{ choice.name }}
          </b-btn>
        </li>
      </ul>
      <div class="px-2 task-record-review-choice-form__alternative-value">
        <b-form-input v-model="alternativeValue" placeholder="Alternative value" />
      </div>
    </fieldset>
  </b-overlay>
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

    &--has-choice:not(&--has-alternative-value) &__alternative-value {
      opacity: 0.25;
    }
  }
</style>
