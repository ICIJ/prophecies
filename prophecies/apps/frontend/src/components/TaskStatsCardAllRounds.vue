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
  }
}
</script>

<template>
  <b-container class="task-stats-card-all-rounds card card-body rounded font-weight-bold">
    <b-row class="pt-2">
      <div
        class="
          task-stats-card-all-rounds__all
          text-center
          text-primary
          col-2
          px-0
        "
      >
        <slot name="title">All</slot>
      </div>
      <b-col class="task-stats-card-all-rounds__stats pr-0">
        <b-row
          class="
            task-stats-card-all-rounds__stats__progress-bar
            col-12
            p-0
            mx-0
            py-2
          "
        >
          <b-progress class="col-12 p-0" :value="progress | round" :max="100" />
        </b-row>
        <b-row class="mt-auto">
          <b-col class="pr-0">
            <span
              class="
                task-stats-card-all-rounds__stats__progress
                bg-primary
                text-white
                text-center
                rounded
                d-inline-block
              "
            >
              {{ progress | round }}%
            </span>
          </b-col>
          <b-col class="pr-0">
            <check-icon size="1x" class="text-primary mr-2" /> {{ done }}
          </b-col>
          <b-col class="pr-0">
            <clock-icon size="1x" class="text-danger mr-2" /> {{ pending }}
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<style lang="scss" scoped>
.task-stats-card-all-rounds {
  padding-left: $spacer-xxl;
  padding-right: $spacer-xxl;
  min-width: 340px;
  max-width: 360px;
  max-height: 93px;
  background-color: $secondary-50;

  &__stats {
    &__progress-bar {
      height: 2em;
      width: 100%;
    }
    &__progress {
      width: 45px;
    }
  }
}
</style>
