<script>
import Cookies from 'js-cookie'
import TaskRecordReviewTutorialStep from '@/components/TaskRecordReviewTutorialStep'

export default {
  name: 'TaskRecordReviewTutorial',
  components: {
    TaskRecordReviewTutorialStep
  },
  data() {
    return {
      showTutorial: undefined,
      stepIndex: 1,
      steps: [{
          text: "Read the content to be checked",
          class: "offset-2 col-8 ",
          width: "130px",
        },
        {
          text: "Check if the predicted value is correct",
          class: "ml-auto col-3",
          width: "180px",
        },
        {
          text: "Select (or type) your choice",
          class: "col-xxl-6 ",
          width: "130px",
        },
        {
          text: "Read others' choice (click one's choice to quickly select the same!)",
          class: "col-lg-6 col-xxl-6 ",
          iconAlign: "float-left",
          width: "250px"
        },
        {
          text: "Comment (you can mention someone with @username or everyone with @project)",
          class: "offset-lg-6 col-lg-5 offset-xxl-6 col-xxl-5 p-0",
          iconAlign: "float-right ",
          width: "350px"
        },
      ]
    }
  },
  created() {
    let showTutorial = Cookies.get('showTutorial')
    if (showTutorial == undefined || showTutorial == "true") {
      showTutorial = true
      Cookies.set('showTutorial', showTutorial, {
        expires: 365,
        sameSite: 'lax'
      })
    } else {
      showTutorial = false
    }
    this.showTutorial = showTutorial;
  },
  computed: {
    isFirstStep() {
      return this.stepIndex == 1
    },
    isLastStep() {
      return this.stepIndex == this.steps.length
    }
  },
  methods: {
    previousTutorialStep() {
      this.stepIndex--
    },
    nextTutorialStep() {
      this.stepIndex++
    },
    closeTutorial() {
      this.showTutorial = false
      Cookies.set('showTutorial', this.showTutorial, {
        expires: 365,
        sameSite: 'lax'
      })
    },
  }
}
</script>
<template>
<b-collapse :visible="showTutorial">
  <div class="task-record-review-tutorial-card card card-body p-4 container-fluid mb-5">
    <div class="row mb-3">
      <div class="col d-flex">
        <div>
          <coffee-icon />
        </div>
        <h2 class=" pl-3 pt-1 first-time-question ">First time here?</h2>
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
          <span class="right-button-width">Next
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
          <div v-if="stepIndex==1 || stepIndex == 2" class="col-lg-4">
            <TaskRecordReviewTutorialStep :index="stepIndex" :step=steps[stepIndex-1] :nb-steps="steps.length" />
          </div>
          <div v-else class="offset-lg-4 col-lg-8">
            <div class="row">
              <div v-if="stepIndex==3" class="col-xxl-6 d-flex justify-content-center ">
                <TaskRecordReviewTutorialStep :index="stepIndex" :step=steps[stepIndex-1] :nb-steps="steps.length" />
              </div>
              <div v-else class="offset-xxl-6 col-xxl-6">
                <TaskRecordReviewTutorialStep :index="stepIndex" :step=steps[stepIndex-1] :nb-steps="steps.length" />
              </div>
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
.task-record-review-tutorial-card {
    background: $light;
    .first-time-question {
        &:after {
            content: "\00a0\00a0";
        }
        text-decoration: underline;
        text-decoration-color: $warning;
        text-decoration-thickness: 5px;
        text-underline-offset: 5px;
        line-height: 24px;
    }
    .right-button-width {
        display: inline-block;
        width: 57px;
    }
}
</style>
