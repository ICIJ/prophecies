<script>
import ChoiceBadge from '@/components/ChoiceBadge.vue'

export default {
  name: 'StatsByRound',
  components: {
    ChoiceBadge
  },
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
    usersStats: {
      type: Array,
      default: () => ([])
    },
    choiceStats: {
      type: Array,
      default: () => ([])
    },
    nbRounds: {
      type: Number,
      default: 1
    }
  },
  filters: {
    round(value) {
      return Math.round(value)
    }
  },
  methods: {
    isNotLastRound(round) {
      return Number(round) !== Number(this.nbRounds)
    },
    roundProgression(value) {
      return `${this.$t('taskStatsCard.roundProgression')}: ${value}%`
    }
  },
  computed: {
    badgeColumnClass() {
      if (this.choiceStats.length > 3) {
        return 'col-3'
      } else if (this.choiceStats.length === 3) {
        return 'col-4'
      } else if (this.choiceStats.length === 2) {
        return 'col-6'
      }
      return ''
    },
    hasUsers() {
      return this.usersStats.length > 0
    },
    label() {
      return this.$t('taskStatsCard.round')
    }
  }
}
</script>

<template>
  <div class="stats-by-round d-flex flex-column" :class="{'stats-by-round--extended':extended}">
    <template v-if="extended">
      <div class="stats-by-round__progress d-flex py-3" :class="hasUsers?'text-primary':'text-secondary'">
        <div class="col-3 pl-0 font-weight-bold  text-nowrap">{{ label }} {{ round }}</div>
        <div class="stats-by-round__progress__value col-9">
          <div v-if="hasUsers" class="py-2">
            <b-progress :value="progress | round" :max="100" :title="roundProgression(progress | round)"/>
          </div>
          <span class="stats-by-round__progress__value--no-record"
                v-else>{{$t('taskStatsCard.noRecordsAssigned')}}</span>
        </div>
      </div>
      <template v-if="hasUsers">
        <slot name="users" v-bind="{users:usersStats}"/>
        <div class="stats-by-round__summary row py-3">
          <div class="stats-by-round__summary__choice d-flex align-items-center " :class="badgeColumnClass"
               v-for="statChoice in choiceStats" :key="statChoice.value">
            <choice-badge
              class="stats-by-round__summary__choice__badge"
              :name="statChoice.name"
              :value="statChoice.value"
              :color="statChoice.color"
            />
            <span class="stats-by-round__number">{{statChoice.progress | round }}</span>%
          </div>
        </div>
      </template>
    </template>
    <template v-else>
        <span class="stats-by-round__progress ">
          {{ label }} {{ round }}
          <span class="stats-by-round__item__value font-weight-bold ml-2 ">
            <span class="stats-by-round__number">{{ progress | round }}</span>%
          </span>
          <span class="text-secondary mx-2" v-if="isNotLastRound(round)">
            |
          </span>
        </span>
    </template>
  </div>
</template>

<style lang="scss">

.stats-by-round {

  &__number {
    font-variant-numeric: tabular-nums;
  }

  &--extended {
    min-width: 340px;
  }

}
</style>
