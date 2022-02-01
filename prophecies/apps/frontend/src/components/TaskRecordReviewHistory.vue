<script>
import { get, uniqueId } from 'lodash'

import User from '@/models/User'
import AlternativeValue from '@/models/AlternativeValue'
import TaskRecordReview from '@/models/TaskRecordReview'
import UserLink from '@/components/UserLink'
import ChoiceBadge from '@/components/ChoiceBadge.vue'

export default {
  name: 'TaskRecordReviewHistory',
  components: {
    UserLink,
    ChoiceBadge
  },
  filters: {
    alternativeValueName (value) {
      const alternativeValue = AlternativeValue.query().where('value', value).first()
      const valueBetweenQuotes = `"${value}"`
      return get(alternativeValue, 'name', valueBetweenQuotes)
    }
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    }
  },
  methods: {
    isMe ({ id = null } = {}) {
      return id === User.me().id
    },
    emitToggleNotes (reviewId) {
      /**
       * Fired when the user toggles the notes
       * @event toggle-notes
       * @param String
       */
      this.$emit('toggle-notes', reviewId)
    },
    selectSameChoice ({ alternativeValue = null, choice } = {}) {
      /**
       * Fired when user selects the same alternative value
       * @event submit
       * @param The changed attributes and relationships
       */
      this.$emit('same', { alternativeValue, choice })
    },
    cancelReview (choice) {
      /**
       * Fired when user cancels their choice
       * @event cancel
       */
      this.$emit('cancel')
    }
  },
  computed: {
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('checker')
        .with('choice')
        .find(this.taskRecordReviewId)
    },
    taskRecordId () {
      return this.taskRecordReview.taskRecordId
    },
    history () {
      const history = TaskRecordReview.query()
        .with('checker')
        .with('choice')
        .where('taskRecordId', this.taskRecordReview.taskRecordId)
        .where(({ id }) => id !== this.taskRecordReview.id)
        .orderBy(({ id }) => -Number(id))
        .get()
      return [this.taskRecordReview, ...history]
    },
    tooltipId () {
      return uniqueId('choice-tooltip-')
    }
  }
}
</script>

<template>
  <div class="task-record-review-history">
    <div class="task-record-review-history__checker d-flex p-1" v-for="{ id, checker, alternativeValue, choice, note } in history" :key="id">
      <div class="task-record-review-history__checker__name" :class="{ 'task-record-review-history__checker__name--is-me': isMe(checker) }">
        <user-link class="text-truncate" :user-id="checker.id">
          {{ checker.displayName }}
          <template v-if="isMe(checker)">
            (you)
          </template>
        </user-link>
      </div>
      <div v-if="choice!==null" class="task-record-review-history__checker__choice">
        <choice-badge :name="choice.name" :value="choice.value" class="task-record-review-history__checker__choice__badge">
          <template #afterTooltip v-if="isMe(checker)">
            |<b-btn size="sm" variant="link" class="text-white" @click="cancelReview(choice)">Cancel my choice</b-btn>
          </template>
        </choice-badge>
      </div>
      <div class="task-record-review-history__checker__alternative-value flex-grow-1">
        <template v-if="alternativeValue">
          <template v-if="isMe(checker)">
            <span class="text-truncate text-dark px-2">
              {{ alternativeValue | alternativeValueName }}
            </span>
          </template>
          <template v-else>
            <b-btn variant="link" class="p-0" @click="selectSameChoice({ alternativeValue, choice })" title="Use the same value" v-b-tooltip.hover>
              <span class="text-truncate text-dark px-2">
                {{ alternativeValue | alternativeValueName }}
              </span>
            </b-btn>
          </template>
        </template>
      </div>
      <b-btn variant="link" size="sm" class="task-record-review-history__checker__note" @click="emitToggleNotes(id)">
        <template v-if="!!note">
          <message-square-icon size="1x" class="mr-1" />1 note
        </template>
        <template v-else-if="isMe(checker)">
          <edit-3-icon size="1x" class="mr-1" />Comment
        </template>
      </b-btn>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-history {

    &__checker {
      min-height: 2.2em;

      &__name, &__choice, &__alternative-value, &__note {
        display: flex;
        align-items: center;
        padding-right: $spacer-sm;
      }

      &__name {
        width: 100%;
        max-width: 100px;
        min-width: 100px;

        &:after {
          content: ":"
        }
      }

      &__alternative-value {
        max-width: 100%;
        min-width: 0;
      }

      &__note {
        padding-bottom: 0;
        padding-top: 0;
        white-space: nowrap;
      }
    }
  }
</style>
