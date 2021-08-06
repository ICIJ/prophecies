<script>
import User from '@/models/User'
import { toVariant } from '@/utils/variant'
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
    }
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    }
  },
  methods: {
    isMe (checker) {
      return checker.id === User.me().id
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
      return this.taskRecordReview.task_record_id
    },
    history () {
      return [this.taskRecordReview, ...this.taskRecordReview.history]
    },
    classList () {
      return {
        'task-record-review-choice-form--has-choice': this.hasChoice,
        'task-record-review-choice-form--has-alternative-value': this.hasAlternativeValue,
        'task-record-review-choice-form--has-note': this.hasNote
      }
    }
  }
}
</script>

<template>
  <div class="task-record-review-history">
    <div class="task-record-review-history__checker d-flex p-1" v-for="{ id, checker, alternative_value, choice, note } in history" :key="id">
      <div class="task-record-review-history__checker__name">
        <span class="text-truncate">
          {{ checker.first_name || checker.username }}
          <template v-if="isMe(checker)">
            (you)
          </template>
        </span>
      </div>
      <div class="task-record-review-history__checker__choice">
        <b-badge class="task-record-review-history__checker__choice__badge" :variant="choice.value | toVariant" v-if="choice">
          {{ choice.name | firstLetter }}<span class="sr-only">{{ choice.name | skipFirstLetter }}</span>
        </b-badge>
      </div>
      <div class="task-record-review-history__checker__alternative-value flex-grow-1">
        <span class="text-truncate">
          {{ alternative_value }}
        </span>
      </div>
      <b-btn variant="link" size="sm" class="task-record-review-history__checker__note" v-if="!!note" @click="$emit('toggle', id)">
        <message-square-icon size="1x" class="mr-1" />1 note
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
