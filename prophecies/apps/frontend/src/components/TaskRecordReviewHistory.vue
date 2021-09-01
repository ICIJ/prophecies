<script>
import { get, orderBy } from 'lodash'

import User from '@/models/User'
import { toVariant } from '@/utils/variant'
import AlternativeValue from '@/models/AlternativeValue'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewHistory',
  filters: {
    toVariant,
    firstLetter (str) {
      return String(str).slice(0, 1)
    },
    skipFirstLetter (str) {
      return String(str).slice(1)
    },
    alternativeValueName (value) {
      const alternativeValue = AlternativeValue.query().where('value', value).first()
      return get(alternativeValue, 'name', value)
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
       * Fired when user select the same alternative value
       * @event submit
       * @param The changed attributes and relationships
       */
      this.$emit('same', { alternativeValue, choice })
    }
  },
  computed: {
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('checker')
        .with('choice')
        .with('history')
        .with('history.checker')
        .with('history.choice')
        .find(this.taskRecordReviewId)
    },
    taskRecordId () {
      return this.taskRecordReview.taskRecordId
    },
    history () {
      const history = [this.taskRecordReview, ...this.taskRecordReview.history]
      return orderBy(history, ({ id }) => -Number(id))
    }
  }
}
</script>

<template>
  <div class="task-record-review-history">
    <div class="task-record-review-history__checker d-flex p-1" v-for="{ id, checker, alternativeValue, choice, note } in history" :key="id">
      <div class="task-record-review-history__checker__name" :class="{ 'task-record-review-history__checker__name--is-me': isMe(checker) }">
        <span class="text-truncate">
          {{ checker.displayName }}
          <template v-if="isMe(checker)">
            (you)
          </template>
        </span>
      </div>
      <div class="task-record-review-history__checker__choice">
        <b-badge class="task-record-review-history__checker__choice__badge" :variant="choice.value | toVariant" v-if="choice" :title="choice.name" v-b-tooltip.right>
          {{ choice.name | firstLetter }}<span class="sr-only">{{ choice.name | skipFirstLetter }}</span>
        </b-badge>
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

      &__name, &__choice, &__alternative-value, &__note {
        display: flex;
        align-items: center;
        padding-right: $spacer-sm;
      }

      &__name {
        width: 100%;
        max-width: 120px;
        min-width: 120px;

        &:after {
          content: ":"
        }
      }

      &__choice {
        width: 100%;
        max-width: 30px;

        & /deep/ .badge {
          padding: 0;
          width: 1.6em;
          height: 1.6em;
          line-height: 1.6em;
        }
      }

      &__alternative-value {
        max-width: 100%;
        min-width: 0;
      }

      &__note {
        white-space: nowrap;
      }
    }
  }
</style>
