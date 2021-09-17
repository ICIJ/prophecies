<script>
export default {
  name: 'TaskRecordReviewTutorialStep',
  props: {
    number: {
      type: Number
    },
    step: {
      type: Object,
      default: () => ({})
    },
    stepCount: {
      type: Number
    }
  },
  computed : {
    isOthersChoiceBlock() {
      return this.number < 4
    }
  }
}
</script>
<template>
<div class="task-record-review-tutorial-step d-flex flex-column align-items-center" :class="step.class">
  <div class="row">
    <b-badge class="task-record-review-tutorial-step__progression" variant="warning">
      <div class="d-block" style="line-height:24px;">
        <div class="float-left ml-2 pr-2 task-record-review-tutorial-step__progression__numbers">{{ number }}/{{ stepCount }}</div>
        <div class="task-record-review-tutorial-step__progression__bar-position px-1">
          <b-progress :value="number" :max="stepCount" />
        </div>
      </div>
    </b-badge>
  </div>
  <div class="task-record-review-tutorial-step__text-content font-weight-bold step-text-content" :style="'width:' + step.width">
    {{ step.text }}
  </div>
  <div v-if="isOthersChoiceBlock" class="text-align-center">
    <arrow-down-icon />
  </div>
  <template v-else>
    <div class="d-none d-xl-block text-align-center">
      <arrow-down-icon />
    </div>
    <div class="d-xl-none container-fluid ">
      <arrow-down-icon :class="step.iconAlign" />
    </div>
  </template>
</div>
</template>

<style lang="scss" scoped>

.task-record-review-tutorial-step {

  &__header {
      display: block;
      width: 60px;
  }

  &__progression {
      font-size: $font-size-lg;
      width: 86px;

      &__bar-position {
          line-height: 24px;
          padding-top: 10px;
          .progress{
            height: 4px;
            &::after{
              top:25%;
            }
          }
      }
  }

  &__text-content {
      text-align: center;
  }
}




</style>
