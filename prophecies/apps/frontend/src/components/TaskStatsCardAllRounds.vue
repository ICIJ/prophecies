<template>
  <div class="task-stats-card-all-rounds">
      All
        <b-progress :value="progress | round" :max="100" />
    <div class="row">
        <span class="task-stats-card-all-rounds__all
            bg-primary
            text-white
            font-weight-bold
            rounded" >
        {{ progress | round }}%
        </span>
        <span class="task-stats-card-all-rounds__done">
            <check-icon class="text-primary" />  {{done}}
        </span>

        <span class="task-stats-card-all-rounds__pending">
            <clock-icon class="text-danger"/>  {{pending}}
        </span>
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
