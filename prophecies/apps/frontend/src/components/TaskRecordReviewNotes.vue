<script>
import { get, find, filter, uniqueId } from 'lodash'
import moment from 'moment'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import TaskRecordReviewNoteTimestamp from '@/components/TaskRecordReviewNoteTimestamp'
import TaskRecordReview from '@/models/TaskRecordReview'
import User from '@/models/User'

export default {
  name: 'TaskRecordReviewNote',
  components: {
    ShortkeyBadge,
    TaskRecordReviewNoteTimestamp
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    highlightedReviewId: {
      type: [String, Number]
    },
    activateShortkeys: {
      type: Boolean
    }
  },
  watch: {
    async autofocus (autofocus) {
      if (autofocus) {
        // The component must be mounted
        await this.$nextTick()
        const selector = '.task-record-review-notes__item__note__form__input'
        this.$el.querySelector(selector).focus()
      }
    }
  },
  data () {
    return {
      inputNote: null
    }
  },
  created () {
    this.inputNote = this.taskRecordReview.note
  },
  computed: {
    autofocus () {
      const checkerId = get(this, 'highlightedReview.checker.id', null)
      return checkerId === User.me().id
    },
    highlightedReview () {
      const id = this.highlightedReviewId
      return find(this.history, { id })
    },
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('checker')
        .find(this.taskRecordReviewId)
    },
    history () {
      const history = TaskRecordReview.query()
        .with('checker')
        .where('taskRecordId', this.taskRecordReview.taskRecordId)
        .where(({ note }) => !!note)
        .where(({ id }) => id !== this.taskRecordReview.id)
        .orderBy('noteCreatedAt', 'desc')
        .get()
      return [this.taskRecordReview, ...history]
    },
    saveNoteLoader () {
      return uniqueId('task-record-review-save-note')
    },
    closeShortkey () {
      if (this.activateShortkeys) {
        return ['esc']
      }
      return []
    },
    noteChanged () {
      return this.inputNote !== this.taskRecordReview.note
    }
  },
  methods: {
    isMe (checker) {
      return checker.id === User.me().id
    },
    async saveInputNoteWithLoader () {
      this.$wait.start(this.saveNoteLoader)
      await this.saveNote()
      this.$wait.end(this.saveNoteLoader)
    },
    async saveNote () {
      const attributes = { note: this.inputNote }
      await TaskRecordReview.api().save(this.taskRecordReviewId, { attributes })
    },
    async handleInputNoteEnter ($event) {
      if (this.noteChanged) {
        $event.target.blur()
        await this.saveInputNoteWithLoader()
      }
    }
  }
}
</script>

<template>
  <div class="task-record-review-notes">
    <b-btn class="task-record-review-notes__close text-muted d-flex align-items-center"
           variant="link"
           quared
           size="sm"
           v-shortkey="closeShortkey"
           @shortkey="$emit('close')"
           @click="$emit('close')">
      <x-icon />
      <shortkey-badge :value="closeShortkey" />
      <span class="sr-only">Close</span>
    </b-btn>
    <div v-for="review in history" :key="review.id" class="task-record-review-notes__item"  :class="{ 'task-record-review-notes__item--highlighted': review.id === highlightedReviewId }">
      <div class="task-record-review-notes__item__checker">
        <span class="text-truncate">
          {{ review.checker.firstName || review.checker.username }}
        </span>
      </div>
      <div class="task-record-review-notes__item__note">
        <template v-if="isMe(review.checker)">
            <form class="task-record-review-notes__item__note__form" @submit.prevent="saveInputNoteWithLoader">
              <fieldset :disabled="$wait.is(saveNoteLoader)">
                <b-overlay :show="$wait.is(saveNoteLoader)" variant="transparent">
                  <b-spinner variant="light" slot="overlay" />
                  <b-form-textarea v-model="inputNote"
                    class="task-record-review-notes__item__note__form__input"
                    placeholder="Type your note here..."
                    rows="2"
                    max-rows="10"
                    @keyup.esc="$emit('close')"
                    @keyup.ctrl.enter="handleInputNoteEnter" />
                </b-overlay>
                <div v-if="noteChanged" class="mt-1 d-flex align-items-center">
                  <b-btn variant="link" size="sm" type="submit" class="text-muted ml-auto">
                    Save
                  </b-btn>
                  <shortkey-badge :value="['Ctrl', 'Enter']" class="ml-2" />
                </div>
                <task-record-review-note-timestamp
                  v-else
                  class="task-record-review-notes__item__note__form__timestamp mt-1"
                  :task-record-review-id="review.id" />
              </fieldset>
            </form>
        </template>
        <template v-else>
          <div class="task-record-review-notes__item__note__wrapper" v-html="review.noteWithMentions"></div>
          <task-record-review-note-timestamp
            class="task-record-review-notes__item__note__timestamp"
            :task-record-review-id="review.id" />
        </template>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  @keyframes highlightNote {
    from {
      background: #fcf3c4;
    }
    to {
      background: #F5F5F5;
    }
  }

  .task-record-review-notes {
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

      @include media-breakpoint-down(xl) {
        position: static;
        margin: 0;
        margin-left: auto;
      }

      &:hover {
        text-decoration: none;
      }
    }

    &__item {
      background: #F5F5F5;
      padding: $spacer-lg $spacer-xl;
      display: flex;
      flex-direction: row;
      align-items: flex-start;
      margin-bottom: $spacer-xl;

      &:last-of-type {
        margin-bottom: 0;
      }

      &--highlighted {
        animation: highlightNote 4s;
      }

      &__note__form__timestamp, &__note__timestamp {
        color: $secondary;
        font-size: $font-size-sm;
        padding: $input-padding-y 0;
        float: right;
      }

      &__checker {
        width: 80px;
        display: flex;
        align-items: center;
        margin-top: $input-border-width;
        padding-top: $input-padding-y;
        padding-right: $spacer-lg;

        &:after {
          content: ":"
        }
      }

      &__note {
        flex-grow: 1;

        &__form {

          &__input {
            width: 100%;
            border-color: transparent;
            background: transparent;
          }
        }

        &__wrapper {
          margin: $input-border-width;
          padding: $input-padding-y $input-padding-x;
        }
      }
    }
  }
</style>
