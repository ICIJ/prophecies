<template>
    <div class="stats-by-users d-flex flex-column flex-grow-1 py-3">
      <div class="stats-by-users__table d-flex flex-row py-3" v-for="(user, index) in users" :key="index">
        <div class="stats-by-users__table__username col-3 pl-0 text-nowrap">
          {{ user.name }}
        </div>
        <div   class="stats-by-users__table__progress text-right mx-3">
          {{ user.progress }}%
        </div>
        <div :class="tableClassList" >
          <check-icon size="1x" class="text-primary mr-2" />{{user.done}}
        </div>
        <div :class="tableClassList"  >
          <clock-icon size="1x" class="text-danger mr-2" />{{user.pending}}
        </div>
      </div>
      <div class="stats-by-users__total d-flex flex-row py-2 font-weight-bold flex-grow-1 align-items-end" >
        <div class="col-3  pl-0">
          Total
        </div>
        <div class="stats-by-users__table__progress text-right mx-3" >
         10%
        </div>
        <div :class="tableClassList">
          <check-icon size="1x" class="text-primary mr-2" />20000
        </div>
        <div :class="tableClassList"  >
          <clock-icon size="1x" class="text-danger mr-2" />30000
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
  computed: {
    tableClassList () {
      return 'd-flex px-3 text-nowrap stats-by-users__table__cell__icon '
    }
  },
  filters: {
    round (value) {
      return Math.round(value)
    }
  }
}
</script>
<style lang="scss" scoped>
.stats-by-users__table
{

  &__progress{
    width: 3em;
    min-width: 3em;
  }
  &__cell__icon{
      align-items: center;
      flex : 0 1 7em;
    }

}
</style>
