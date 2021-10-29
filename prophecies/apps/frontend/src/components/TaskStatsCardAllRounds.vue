<template>
  <div class="task-stats-card-all-rounds card rounded card-body">
    <div class="container p-0">
      <div class="row justify-content-end">
        <div class="task-stats-card-all-rounds__all text-right ">
          All
        </div>

        <div class="col-9">
          <div class="task-stats-card-all-rounds__progress py-2">
            <b-progress :value="progress | round" :max="100" />
          </div>
        </div>
      </div>
      <div class="row font-weight-bold text-center justify-content-end">
        <div class="col-3  ">
          <span class=" p-1
            bg-primary
            text-white
            rounded" >
            {{ progress | round }}%
          </span>
        </div>
        <div class="col-3">
          <check-icon size="1.3x" class="text-primary mr-2" />  {{done}}
        </div>
        <div class="col-3">
          <clock-icon size="1.3x" class="text-danger mr-2" />  {{pending}}
        </div>

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
    round: {
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
    min-width: 425px;
    max-width: 450px;

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
