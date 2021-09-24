<script>
import store from '@/store'
import TaskRecordReviewTutorialStep from '@/components/TaskRecordReviewTutorialStep'

export default {
  name: 'TaskRecordReviewTutorial',
  components: {
    TaskRecordReviewTutorialStep
  },
  data () {
    return {
      stepNumber: 1,
      steps: [{
        text: 'Read the content',
        class: 'offset-2 col-8 ',
        width: '130px'
      },
      {
        text: 'Check whether the predicted value is correct',
        class: 'ml-auto col-3',
        width: '180px'
      },
      {
        text: 'Select (or type) your choice',
        class: 'col-xxl-6 ',
        width: '130px'
      },
      {
        text: "Read others' choices (click another user's choice to select the same!)",
        class: 'col-lg-6 col-xxl-6 ',
        iconAlign: 'float-left',
        width: '250px'
      },
      {
        text: 'Comment (you can mention other checkers with @username, or everyone with @project)',
        class: 'offset-lg-6 col-lg-5 offset-xxl-6 col-xxl-5 p-0',
        iconAlign: 'float-right ',
        width: '350px'
      }
      ]
    }
  },
  computed: {
    isFirstStep () {
      return this.stepNumber === 1
    },
    isLastStep () {
      return this.stepNumber === this.steps.length
    },
    isLeftBlock () {
      return this.stepNumber === 1 || this.stepNumber === 2
    },
    isChoiceBlock () {
      return this.stepNumber === 3
    },
    showTutorial :{
      get(){
        return store.state.app.showTutorial
      },
      set(isVisible){
        store.dispatch("app/showTutorial", isVisible)
      }
    }
  },
  methods: {
    previousTutorialStep () {
      this.stepNumber--
    },
    nextTutorialStep () {
      this.stepNumber++
    },
    closeTutorial () {
      this.showTutorial = false
    }
  }
}
</script>

<template>
<b-collapse :visible="showTutorial">
  <div class="task-record-review-tutorial card card-body p-4 container-fluid mb-5">
    <div class="row mb-3">
      <div class="col d-flex task-record-review-tutorial__header">
        <div>
          <coffee-icon />
        </div>
        <h2 class=" pl-3 pt-1 task-record-review-tutorial__first-time-question ">First time here?</h2>
      </div>

      <div class="col-auto task-record-review-tutorial-card__buttons">
        <b-btn
        @click="closeTutorial()"
        class="mr-3 task-record-review-tutorial-card__buttons__skip"
        size="sm"
        v-if="!isLastStep"
        variant="link"
        >Skip tutorial</b-btn>
        <b-btn
          @click="previousTutorialStep()"
          class="mr-3 task-record-review-tutorial-card__buttons__previous"
          v-if="!isFirstStep"
          variant="outline-primary"
        >
          <arrow-left-icon size="1x" class="mr-1" /> Previous
        </b-btn>
        <b-btn
          @click="nextTutorialStep()"
          class="task-record-review-tutorial-card__buttons__next font-weight-bold"
          v-if="!isLastStep"
          variant="warning"
        >
          <span class="task-record-review-tutorial__right-button-width">Next
            <arrow-right-icon size="1x" />
          </span>
        </b-btn>
        <b-btn
          @click="closeTutorial()"
          class="task-record-review-tutorial-card__buttons__close font-weight-bold"
          v-else
          variant="warning"
        >
          <span class="right-button-width">Close
            <XIcon size="1x" />
          </span>
        </b-btn>
      </div>
    </div>
    <div class="row no-gutters ">
      <div class="col flex-grow-1">
        <div class="row no-gutters">
          <div v-if="isLeftBlock" class="col-lg-4">
            <task-record-review-tutorial-step :number="stepNumber" :step="steps[stepNumber-1]" :step-count="steps.length" />
          </div>
          <div v-else class="offset-lg-4 col-lg-8">
            <div class="row">
              <div v-if="isChoiceBlock" class="col-xxl-6 d-flex justify-content-center ">
                <task-record-review-tutorial-step :number="stepNumber" :step="steps[stepNumber-1]" :step-count="steps.length" />
              </div>
              <div v-else class="offset-xxl-6 col-xxl-6">
                <task-record-review-tutorial-step :number="stepNumber" :step="steps[stepNumber-1]" :step-count="steps.length" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</b-collapse>
</template>

<style lang="scss" scoped>
.task-record-review-tutorial {
    background: rgba($primary, .1);

    &__header{
      color:$primary;
    }

    &__first-time-question {
        text-decoration: underline;
        text-decoration-color: $warning;
        text-decoration-thickness: 5px;
        text-underline-offset: 5px;
        line-height: 24px;

        &:after {
            content: "\00a0\00a0";
        }
    }

    &__right-button-width {
        display: inline-block;
        width: 57px;
    }
}
</style>
