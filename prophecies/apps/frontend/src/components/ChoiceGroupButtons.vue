<script>
import { toVariant } from '@/utils/variant'
import ChoiceGroup from '@/models/ChoiceGroup'
import ShortkeyBadge from '@/components/ShortkeyBadge'

export default {
  name: 'ChoiceGroupButtons',
  model: {
    prop: 'choiceId',
    event: 'update:choiceId'
  },
  props: {
    choiceId: {
      type: [String, Number],
      default: null
    },
    choiceGroupId: {
      type: [String, Number]
    },
    activateShortkeys: {
      type: Boolean
    }
  },
  filters: {
    toVariant
  },
  components: {
    ShortkeyBadge
  },
  computed: {
    choiceGroup () {
      return ChoiceGroup
        .query()
        .with('choices')
        .find(this.choiceGroupId)
    },
    hasChoice () {
      return this.choiceId !== null
    }
  },
  methods: {
    selectChoice ({ id }) {
      /**
         * Fired when the user selected a choice
         * @event update:choiceId
         * @param The selected choice
         */
      this.$emit('update:choiceId', id)
    },
    choiceIsSelected ({ id }) {
      return id === this.choiceId
    },
    choiceClassList (choice) {
      return {
        'choice-group-buttons__item--selected': this.choiceIsSelected(choice)
      }
    },
    choiceShortkeys ({ shortkeys = null }) {
      if (!this.activateShortkeys || !shortkeys) {
        return null
      }
      return shortkeys.split(',')
    }
  }
}
</script>

<template>
  <ul class="choice-group-buttons list-unstyled row"
     :class="{ 'choice-group-buttons--has-choice': this.hasChoice }">
    <li v-for="choice in choiceGroup.choices"
        class="col choice-group-buttons__item pb-3"
        :class="choiceClassList(choice)"
        :key="choice.id">
      <b-btn @click="selectChoice(choice)"
             @shortkey="selectChoice(choice)"
             v-shortkey="choiceShortkeys(choice)"
             block
             class="choice-group-buttons__item__button text-nowrap"
             :variant="choice.value | toVariant">
        {{ choice.name }}
        <template v-if="choiceShortkeys(choice)">
          <shortkey-badge class="ml-1" :value="choice.shortkeys" />
        </template>
      </b-btn>
    </li>
  </ul>
</template>

<style lang="scss" scoped>
  .choice-group-buttons {
    margin: 0 -$spacer-xs;
    margin-bottom: 0;

    &__item {
      font-weight: normal;
      padding: 0 $spacer-xs;
      transition: $transition-fade;

      &__button /deep/ .shortkey-badge {
        color: inherit;
      }
    }

    .choice-group-buttons--has-choice:not(:hover) &__item:not(&__item--selected) {
      opacity: 0.25;
    }

    .choice-group-buttons--has-choice &__item--selected {
      opacity: 1;
      font-weight: bold;
    }
  }
</style>
