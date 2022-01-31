<template>
    <div class="stats-by-users d-flex flex-column flex-grow-1 py-3">
      <div class="stats-by-users__table d-flex flex-row py-3" v-for="(user, index) in users" :key="index">
        <div class="stats-by-users__table__username col-3 px-0 text-nowrap">
          {{ user.name }}
        </div>
        <div class="stats-by-users__table__progress text-right mx-3">
          <span class="stats-by-users__table__number">{{ user.progress | round}}</span>%
        </div>
        <div :class="tableClassList">
          <check-icon size="1x" class="text-primary mr-2" /><span class="stats-by-users__table__number">{{user.done}}</span>
        </div>
        <div :class="tableClassList"  >
          <clock-icon size="1x" class="text-danger mr-2" /><span class="stats-by-users__table__number">{{user.pending}}</span>
        </div>
      </div>
      <div class="stats-by-users__total d-flex flex-row py-2 font-weight-bold flex-grow-1 align-items-end" >
        <div class="col-3 pl-0">
          Total
        </div>
        <div class="stats-by-users__table__progress text-right mx-3" >
        <span class="stats-by-users__table__number">{{ totalStats.progress | round}}</span>%
        </div>
        <div :class="tableClassList">
          <check-icon size="1x" class="text-primary mr-2" /><span class="stats-by-users__table__number">{{ totalStats.done }}</span>
        </div>
        <div :class="tableClassList"  >
          <clock-icon size="1x" class="text-danger mr-2" /><span class="stats-by-users__table__number">{{ totalStats.pending }}</span>
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
    },
    totalStats () {
      return this.users.reduce((acc, user) => ({
        done: acc.done + user.done,
        pending: acc.pending + user.pending,
        progress: acc.progress + user.progress
      }), { done: 0, pending: 0, progress: 0 })
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
  &__number{
    font-variant-numeric: tabular-nums;
  }
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
