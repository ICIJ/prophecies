<script>
import { formatDateFromNow, formatDateLong } from '@/utils/date'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import Action from '@/models/Action'

export default {
  name: 'TaskRecordChanges',
  components: {
    ShortkeyBadge
  },
  filters: {
    formatDateLong(d) {
      return formatDateLong(d)
    },
    formatDateFromNow(d) {
      return formatDateFromNow(d)
    }
  },
  props: {
    actionIds: {
      type: Array,
      default: () => []
    },
    activateShortkeys: {
      type: Boolean
    }
  },
  computed: {
    actions() {
      return Action.query()
        .with('actor')
        .with('target')
        .with('actionObject')
        .orderBy('timestamp', 'desc')
        .whereIdIn(this.actionIds)
        .get()
    },
    closeShortkey() {
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
    <b-btn
      v-shortkey.propagate="closeShortkey"
      class="task-record-review-changes__close text-muted d-flex align-items-center"
      variant="link"
      squared
      size="sm"
      @shortkey="$emit('close')"
      @click="$emit('close')"
    >
      <x-icon />
      <shortkey-badge :value="closeShortkey" />
      <span class="sr-only">Close</span>
    </b-btn>
    <div class="task-record-review-changes__actions">
      <div
        v-if="!actions.length"
        class="task-record-review-changes__actions__item task-record-review-changes__actions__item--empty"
      >
        No changes on this record yet.
      </div>
      <div v-for="action in actions" :key="action.id" class="task-record-review-changes__actions__item d-flex">
        <div class="task-record-review-changes__actions__item__content flex-grow-1 text-truncate mr-1">
          <span v-html="$t(action.i18n, { ...action.data, ...action })"></span>
        </div>
        <div
          v-b-tooltip.hover
          class="task-record-review-changes__actions__item__timestamp text-secondary text-nowrap"
          :title="action.timestamp | formatDateLong"
        >
          {{ action.timestamp | formatDateFromNow }}
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.task-record-review-changes {
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
    background: #f5f5f5;

    &:hover {
      text-decoration: none;
    }

    @include media-breakpoint-down(xl) {
      position: static;
      margin: 0;
      margin-left: auto;
    }
  }

  &__actions {
    padding: $spacer-sm $spacer-xl 0;
    background: #f5f5f5;
    max-height: calc(10vh + 200px);
    overflow: auto;

    &__item {
      margin-bottom: $spacer-sm;
    }
  }
}
</style>
