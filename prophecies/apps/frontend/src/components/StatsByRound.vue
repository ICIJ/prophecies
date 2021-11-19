<template>
  <div class="stats-by-round d-flex flex-column" :class="{'stats-by-round--extended':extended}">
    <template v-if="extended">
      <div class="stats-by-round__progress d-flex  py-3">
        <div class="col-3 pl-0 font-weight-bold text-primary text-nowrap">Round {{ round }}</div>
        <div class="stats-by-round__progress__value col-9 py-2"> <b-progress :value="progress | round" :max="100" /></div>
      </div>
      <stats-by-users :users="users" />
      <div class="stats-by-round__summary row py-3">
        <div class="stats-by-round__summary__choice d-flex align-items-center" :class="badgeColumnClass" v-for="choice in choices" :key="choice.value">
          <b-badge class="stats-by-round__summary__choice__badge mr-3 " :variant="choice.value | toVariant" v-if="choice" :title="choice.name" v-b-tooltip.right>
            {{ choice.name | firstLetter }}<span class="sr-only">{{ choice.name | skipFirstLetter }}</span>
          </b-badge>{{choice.progress}}%
        </div>
      </div>
    </template>
    <template v-else>
      <span class="stats-by-round__progress ">
        {{ $t('taskStatsCard.round') }} {{ round }}
        <span class="stats-by-round__item__value font-weight-bold ml-2 ">
          {{ progress | round }}%
        </span>
        <span class="text-secondary mx-2" v-if="Number(round) !== Number(nbRounds)">
          |
        </span>
      </span>
    </template>
  </div>
</template>

<script>
import { toVariant } from '@/utils/variant'
import StatsByUsers from '@/components/StatsByUsers.vue'

export default {
  name: 'StatsByRound',
  props: {
    extended: {
      type: Boolean,
      default: false
    },
    round: {
      type: Number
    },
    progress: {
      type: Number
    },
    choices: {
      type: Array,
      default: () => ([])
    },
    users: {
      type: Array,
      default: () => ([])
    },
    summary: {
      type: Array,
      default: () => ([])
    },
    nbRounds: {
      type: Number,
      default: 0
    }
  },
  components: {
    StatsByUsers
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
  computed: {
    badgeColumnClass () {
      return this.choices.length ? `col-${12 / this.choices.length}` : ''
    }
  }
}
</script>

<style lang="scss">

.stats-by-round
{
  &--extended{
    min-width: 340px;
  }

  &__summary__choice__badge{
    width:1.5em;
    height:1.5em;
    display: inline-block;
  }
}
</style>
