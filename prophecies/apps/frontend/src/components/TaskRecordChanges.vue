<script>
import moment from 'moment'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import Action from '@/models/Action'

export default {
  name: 'TaskRecordChanges',
  components: {
    ShortkeyBadge
  },
  props: {
    actionIds: {
      type: Array,
      default: () => ([])
    },
    activateShortkeys: {
      type: Boolean
    }
  },
  filters: {
    formatDateLong (d) {
      return moment(d).format('MMM Do YYYY - hh:mm')
    },
    formatDateFromNow (d) {
      return moment(d).fromNow()
    }
  },
  computed: {
    actions () {
      return Action
        .query()
        .with('actor')
        .with('target')
        .with('actionObject')
        .orderBy('timestamp', 'desc')
        .whereIdIn(this.actionIds)
        .get()
    },
    closeShortkey () {
      if (this.activateShortkeys) {
        return ['esc']
      }
      return []
    }
  }
}
</script>

<template>
  <div class="task-record-review-changes">
    <b-btn class="task-record-review-changes__close text-muted d-flex align-items-center"
           variant="link"
           squared
           size="sm"
           v-shortkey.propagate="closeShortkey"
           @shortkey="$emit('close')"
           @click="$emit('close')">
      <x-icon />
      <shortkey-badge :value="closeShortkey" />
      <span class="sr-only">Close</span>
    </b-btn>
    <div class="task-record-review-changes__actions">
      <div class="task-record-review-changes__actions__item task-record-review-changes__actions__item--empty" v-if="!actions.length">
        No changes on this record yet.
      </div>
      <div v-for="action in actions" :key="action.id" class="task-record-review-changes__actions__item d-flex">
        <div class="task-record-review-changes__actions__item__content flex-grow-1">
          <span class="text-truncate" v-html="$t(action.i18n, { ...action.data, ...action })"></span>
        </div>
        <div class="task-record-review-changes__actions__item__timestamp text-secondary" :title="action.timestamp | formatDateLong" v-b-tooltip.hover>
          {{ action.timestamp | formatDateFromNow }}
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-changes {
    max-width: 630px;
    margin: auto;
    position: relative;
    padding: $spacer-xs 0 0;
    display: flex;
    flex-direction: column;

    &__close {
      position: absolute;
      top: $spacer-xs;
      left: 100%;
      margin-left: $spacer;
      background: #F5F5F5;

      &:hover {
        text-decoration: none;
      }

      @media (max-width: 860px) {
        position: static;
        margin: 0;
        margin-left: auto;
      }
    }

    &__actions {
      padding: $spacer-sm $spacer-xl 0;
      background: #F5F5F5;

      &__item {
        margin-bottom: $spacer-sm;
      }
    }
  }
</style>
