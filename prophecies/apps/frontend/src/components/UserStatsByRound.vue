<template>
  <div class="user-stats-by-round d-flex flex-column py-3">
    <div class="user-stats-by-round__progress d-flex flex-row py-4">
       <div class="col-3 pl-0 font-weight-bold text-primary">Round {{ round }}</div>
     <div class="col-9 py-2"> <b-progress :value="progress | round" :max="100" /></div>
    </div>
    <div class="user-stats-by-round__users d-flex flex-column">
      <div class="d-flex flex-row py-2" v-for="(user, index) in users" :key="index">
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
      <div class="user-stats-by-round__total d-flex flex-row py-2 font-weight-bold " >
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
    <div class="user-stats-by-round__summary row">
      <div class="user-stats-by-round__summary__choice" :class="badgeColumnClass" v-for="choice in choices" :key="choice.value">
        <b-badge class="task-record-review-history__checker__choice__badge" :variant="choice.value | toVariant" v-if="choice" :title="choice.name" v-b-tooltip.right>
          {{ choice.name | firstLetter }}<span class="sr-only">{{ choice.name | skipFirstLetter }}</span>
        </b-badge>{{choice.progress}}%
      </div>
    </div>
  </div>
</template>

<script>
import { toVariant } from '@/utils/variant'

export default {
  name: 'UserStatsByRound',
  props: {
    round: {
      type: Number
    },
    progress: {
      type: Number
    },
    choices: {
      type: Array,
      default:()=>([])
    },
    users: {
      type: Array,
      default:()=>([])
    },
    summary: {
      type: Array,
      default:()=>([])
    }
  },
  filters: {
    toVariant,
    firstLetter (str) {
      return String(str).slice(0, 1)
    },
    skipFirstLetter (str) {
      return String(str).slice(1)
    },
    round (value) {
      return Math.round(value)
    }
  },
  data () {
    return {

    }
  },
  computed: {
    badgeColumnClass(){
      return this.choices.length?`col-${12/this.choices.length}`:'';
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
