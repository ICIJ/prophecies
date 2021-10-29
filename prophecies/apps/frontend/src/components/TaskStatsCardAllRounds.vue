<template>
  <div class="task-stats-card-all-rounds card card-body rounded ">
    <div class="d-flex flex-row">
      <div class="col-1 task-stats-card-all-rounds__all text-right px-0">
        All
      </div>
        <div class="col-11 task-stats-card-all-rounds__progress py-2">
          <b-progress :value="progress | round" :max="100" />
        </div>
    </div>
    <div class="d-flex flex-row font-weight-bold text-center ">
      <div class="offset-1 col-3 px-0">
        <span class=" p-1
          bg-primary
          text-white
          rounded" >
          {{ progress | round }}%
        </span>
      </div>
      <div class="col-4 px-0">
        <check-icon size="1x" class="text-primary mr-2" />  {{done}}
      </div>
      <div class="col-4  px-0">
        <clock-icon size="1x" class="text-danger mr-2" />  {{pending}}
      </div>

    </div>
  </div>
</template>

<script>

export default {
  name: 'TaskStatsCardAllRounds',
  props: {
    progress: {
      type: Number
    },
    done: {
      type: Number
    },
    pending: {
      type: Number
    }
  },
  filters: {
    round (value) {
      return Math.round(value)
    }
  },
  computed: {

  }
}
</script>

<style lang="scss" scoped>
  .task-stats-card-all-rounds {
padding-left: 48px;
padding-right: 48px;
width:370px;
min-width:370px;
max-width:370px;
      background-color: $secondary-50;

    &__all {
      color: $primary;
      font-weight: bold;
    }

    &__progress {
      height: 2em;
    }
  }
</style>
