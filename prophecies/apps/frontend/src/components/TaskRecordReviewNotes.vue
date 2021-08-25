<script>
import { filter, uniqueId } from 'lodash'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import TaskRecordReview from '@/models/TaskRecordReview'
import User from '@/models/User'

export default {
  name: 'TaskRecordReviewNote',
  components: {
    ShortkeyBadge
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    autofocus: {
      type: Boolean
    }
  },
  watch: {
    async autofocus (autofocus) {
      if (autofocus) {
        // The component must be munted
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
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('checker')
        .with('history')
        .with('history.checker')
        .with('history.choice')
        .find(this.taskRecordReviewId)
    },
    history () {
      const historyWithNotes = filter(this.taskRecordReview.history, ({ note }) => !!note)
      return [this.taskRecordReview, ...historyWithNotes]
    },
    saveNoteLoader () {
      return uniqueId('task-record-review-save-note')
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
      if (($event.metaKey || $event.ctrlKey) && $event.keyCode === 13) {
        $event.target.blur()
        await this.saveInputNoteWithLoader()
      }
    }
  }
}
</script>

<template>
  <div class="task-record-review-notes">
    <b-btn class="task-record-review-notes__close text-muted" variant="link" squared size="sm" @click="$emit('close')">
      <x-icon />
      <span class="sr-only">Close</span>
    </b-btn>
    <div v-for="{ id, checker, note } in history" :key="id" class="task-record-review-notes__item">
      <div class="task-record-review-notes__item__checker">
        <span class="text-truncate">
          {{ checker.firstName || checker.username }}
        </span>
      </div>
      <div class="task-record-review-notes__item__note">
        <template v-if="isMe(checker)">
            <form class="task-record-review-notes__item__note__form" @submit.prevent="saveInputNoteWithLoader">
              <fieldset :disabled="$wait.is(saveNoteLoader)">
                <b-overlay :show="$wait.is(saveNoteLoader)" variant="transparent">
                  <b-spinner variant="light" slot="overlay" />
                  <b-form-textarea v-model="inputNote"
                    class="task-record-review-notes__item__note__form__input"
                    placeholder="Type your note here..."
                    rows="2"
                    max-rows="10"
                    @keyup.enter="handleInputNoteEnter" />
                </b-overlay>
                <b-collapse :visible="inputNote !== note">
                  <div class="mt-1 d-flex align-items-center">
                    <b-btn variant="link" size="sm" type="submit" class="text-muted ml-auto">
                      Save
                    </b-btn>
                    <shortkey-badge :value="['Meta', 'Enter']" class="ml-2" />
                  </div>
                </b-collapse>
              </fieldset>
            </form>
        </template>
        <template v-else>
          <div class="task-record-review-notes__item__note__wrapper">
            {{ note }}
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .task-record-review-notes {
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


      @media (max-width: 860px) {
        position: static;
        margin: 0;
        margin-left: auto;
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

      &__checker {
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
