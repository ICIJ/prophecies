<template>
    <div class="stats-by-users d-flex flex-column flex-grow-1">
      <div class="stats-by-users__table d-flex flex-row py-2" v-for="(user, index) in users" :key="index">
        <div class="col-3  pl-0">
          {{ user.name }}
        </div>
        <div  class="col-3">
          {{ user.progress }}%
        </div>
        <div class="col-3">
          <check-icon size="1x" class="text-primary mr-2" />{{user.done}}
        </div>
        <div class="col-3" >
          <clock-icon size="1x" class="text-danger mr-2" />{{user.pending}}
        </div>
      </div>
      <div class="stats-by-users__total d-flex flex-row py-2 font-weight-bold flex-grow-1 align-items-end" >
        <div class="col-3  pl-0">
          Total
        </div>
        <div  class="col-3">
         10%
        </div>
        <div class="col-3">
          <check-icon size="1x" class="text-primary mr-2" />20
        </div>
        <div class="col-3" >
          <clock-icon size="1x" class="text-danger mr-2" />30
        </div>
      </div>
    </div>
</template>

<script>

export default {
  name: 'StatsByUsers',
  props: {
    users: {
      type: Array,
      default: () => ([])
    }
  },
  filters: {
    round (value) {
      return Math.round(value)
    }
  }
}
</script>
