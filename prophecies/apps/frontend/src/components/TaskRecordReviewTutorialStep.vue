<script>
export default {
  name: 'TaskRecordReviewTutorialStep',
  props: {
    index: {
      type: Number
    },
    step: {
      type: Object,
      default: () => ({})
    },
    nbSteps: {
      type: Number
    }
  }
}
</script>
<template>
<div class="d-flex flex-column align-items-center" :class="step.class">
  <div class="row">
    <b-badge class="step-progression" variant="warning">
      <div class="d-block" style="line-height:24px;">
        <div class="float-left pr-1 step-progression__numbers">{{index}}/{{nbSteps}}</div>
        <div class="step-progression__bar-position">
          <b-progress :value="index" :max="nbSteps"></b-progress>
        </div>
      </div>
    </b-badge>
  </div>
  <div class="step-text-content font-weight-bold step-text-content" :style="'width:'+step.width">
    {{step.text}}
  </div>
  <div v-if="index<4" class="text-align-center">
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
.step-header {
    display: block;
    width: 60px;
}
.step-progression {
    font-size: $font-size-lg;
    width: 70px;

    &__bar-position {
        line-height: 24px;
        padding-top: 5px;
    }
}



.step-text-content {
    text-align: center;
}
</style>
