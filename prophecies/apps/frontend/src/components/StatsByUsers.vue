<template>
    <div class="stats-by-users d-flex flex-column flex-grow-1 py-3">
      <div class="stats-by-users__row d-flex flex-row py-2" v-for="(user, index) in users" :key="index">
        <div class="stats-by-users__row__username col-3 px-0 text-nowrap">
          {{ user.name }}
        </div>
        <div class="stats-by-users__row__progress text-right mx-3">
          <span class="stats-by-users__row__number">{{ user.progress | round}}</span>%
        </div>
        <div class="stats-by-users__row__done " :class="tableClassList">
          <span class="stats-by-users__row__number">{{user.done}}</span><check-icon size="1x" class="text-primary ml-2" />
        </div>
        <div class="stats-by-users__row__pending" :class="tableClassList"  >
          <span class="stats-by-users__row__number">{{user.pending}}</span><clock-icon size="1x" class="text-danger ml-2" />
        </div>
      </div>
      <div v-if="withTotal" class="stats-by-users__total d-flex flex-row py-3 font-weight-bold flex-grow-1 align-items-end" >
        <div class="col-3 pl-0">
          Total
        </div>
        <div class="stats-by-users__row__progress text-right mx-3" >
        <span class="stats-by-users__row__number">{{ totalStats.progress | round}}</span>%
        </div>
        <div :class="tableClassList">
          <span class="stats-by-users__row__number">{{ totalStats.done }}</span><check-icon size="1x" class="text-primary ml-2" />
        </div>
        <div :class="tableClassList"  >
          <span class="stats-by-users__row__number">{{ totalStats.pending }}</span><clock-icon size="1x" class="text-danger ml-2" />
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
    },
    withTotal: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    computeStats (users) {
      return users.reduce((acc, user) => ({
        done: acc.done + user.done,
        pending: acc.pending + user.pending,
        progress: acc.progress + (user.progress / users.length)
      }), { done: 0, pending: 0, progress: 0 })
    }
  },
  computed: {
    tableClassList () {
      return 'd-flex px-3 text-nowrap stats-by-users__row__cell__icon '
    },
    totalStats () {
      return this.computeStats(this.users)
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
.stats-by-users__row
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
      justify-content:right;
      flex : 0 1 7em;
    }
}
</style>
