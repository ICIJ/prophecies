<script>
import {get, isBoolean, uniqueId} from 'lodash'
import TaskRecordChanges from '@/components/TaskRecordChanges'
import TaskRecordReviewActions from '@/components/TaskRecordReviewActions'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'
import TaskRecordReviewHistory from '@/components/TaskRecordReviewHistory'
import TaskRecordReviewNotes from '@/components/TaskRecordReviewNotes'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import Action from '@/models/Action'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCard',
  components: {
    ShortkeyBadge,
    TaskRecordChanges,
    TaskRecordReviewActions,
    TaskRecordReviewChoiceForm,
    TaskRecordReviewHistory,
    TaskRecordReviewNotes
  },
  props: {
    taskRecordReviewId: {
      type: [String, Number]
    },
    active: {
      type: Boolean
    },
    selected: {
      type: Boolean
    },
    previewLink: {
      type: Boolean
    },
    frozen: {
      type: Boolean
    },
    highlightNote: {
      type: [Boolean, String]
    }
  },
  data() {
    return {
      showChanges: false,
      showNotes: false,
      highlightedReviewId: null,
      actionIds: []
    }
  },
  watch: {
    isLoading() {
      this.showChanges = false
      this.showNotes = false
      this.$root.$emit('bv::hide::tooltip')
    },
    active() {
      this.$shortkey.toggle(this.active)
    }
  },
  created() {
    this.toggleNotes(!!this.highlightNote, this.initialHighlightedReviewId)
    this.$shortkey.bind('ctrl+l', () => this.openLink())
    this.$shortkey.bind('ctrl+alt+n', () => this.toggleNotes())
    this.$shortkey.toggle(this.active)
  },
  methods: {
    async selectChoiceWithLoader(data) {
      this.$wait.start(this.loader)
      await this.selectChoice(data)
      this.$wait.end(this.loader)
    },
    async selectChoice(data) {
      try {
        if (data) {
          // We use a dedicated method that will format the data for the JSONAPI spec
          // and return the updated object (the store shall be updated as well).
          await TaskRecordReview.api().selectChoice(this.taskRecordReviewId, data)
        } else {
          await TaskRecordReview.api().cancelChoice(this.taskRecordReviewId)
        }
        // Hide node to avoid using unecessary space
        this.showNotes = false
        // Let parent component know about the update
        this.emitUpdate()
      } catch (_) {
        const variant = 'danger'
        const title = 'Something went wrong'
        const message = 'Unable to update your review.'
        this.makeToast(variant, title, message)
      }
    },
    async lock() {
      try {
        await TaskRecord.api().lock(this.taskRecord.id)
        // Let parent component know about the update
        this.emitUpdate()
      } catch (error) {
        this.displayError(error)
      }
    },
    async lockWithLoader() {
      this.$wait.start(this.loader)
      await this.lock()
      this.$wait.end(this.loader)
    },
    async unlock() {
      try {
        await TaskRecord.api().unlock(this.taskRecord.id)
        // Let parent component know about the update
        this.emitUpdate()
      } catch (error) {
        this.displayError(error)
      }
    },
    async unlockWithLoader() {
      this.$wait.start(this.loader)
      await this.unlock()
      this.$wait.end(this.loader)
    },
    async bookmark() {
      try {
        await TaskRecord.api().bookmark(this.taskRecord.id)
      } catch (error) {
        this.displayError(error)
      }
    },
    async unbookmark() {
      try {
        await TaskRecord.api().unbookmark(this.taskRecord.id)
      } catch (error) {
        this.displayError(error)
      }
    },
    async fetchTaskRecordActions() {
      const taskRecordId = this.taskRecordReview.taskRecordId
      const {response} = await Action.api().forTaskRecord(taskRecordId)
      this.actionIds = get(response, 'data.data', []).map(a => a.id)
    },
    async fetchTaskRecordActionsWithLoader() {
      this.$wait.start(this.loader)
      await this.fetchTaskRecordActions()
      this.$wait.end(this.loader)
    },
    async fetchAndToggleChanges(toggler = null) {
      if (!this.showChanges || toggler) {
        await this.fetchTaskRecordActionsWithLoader()
      }
      this.toggleChanges(toggler)
    },
    async toggleChanges(toggler = null) {
      this.showChanges = toggler !== null ? !!toggler : !this.showChanges
    },
    toggleNotes(toggler = null, highlightedReviewId) {
      if (!this.showNotes || toggler) {
        this.showChanges = false
        this.highlightedReviewId = highlightedReviewId
      }
      this.showNotes = toggler !== null ? !!toggler : !this.showNotes
    },
    highlightAndToggleNotes(highlightedReviewId) {
      if (this.highlightedReviewId !== highlightedReviewId) {
        return this.toggleNotes(true, highlightedReviewId)
      }
      return this.toggleNotes(!this.showNotes, highlightedReviewId)
    },
    makeToast(variant = null, title, text) {
      this.$bvToast.toast(text, {title, variant, appendToast: true})
    },
    emitUpdate() {
      /**
       * Fired when the task record review is updated
       * @event update
       */
      this.$emit('update')
    },
    openLink() {
      if (this.link) {
        window.open(this.link)
      }
    },
    displayError(error) {
      const message = get(error, 'response.data.errors[0].detail')
      const variant = 'warning'
      const title = `⛔ Task record #${this.taskRecord.id}`
      this.makeToast(variant, title, message)
    }
  },
  computed: {
    showLinkPreview() {
      return !this.showNotes && !this.showChanges && this.previewLink && !!this.taskRecord?.embeddableLink
    },
    initialHighlightedReviewId() {
      // If the `highlightNote` is a boolean, we highlight
      // the current task record review by default
      if (isBoolean(this.highlightNote)) {
        return this.highlightNote ? this.taskRecordReviewId : null
      }
      return this.highlightNote
    },
    isLoading() {
      return this.frozen || this.$wait.is(this.loader)
    },
    selectedInput: {
      get() {
        return this.selected
      },
      set(value) {
        return this.$emit('update:selected', value)
      }
    },
    taskRecordReview() {
      const trr = TaskRecordReview
        .query()
        .with('taskRecord')
        .find(this.taskRecordReviewId)
      return trr
    },
    taskRecord() {
      return get(this, 'taskRecordReview.taskRecord')
    },
    link() {
      return get(this, 'taskRecordReview.taskRecord.link')
    },
    embeddableLink() {
      return get(this, 'taskRecordReview.taskRecord.embeddableLink')
    },
    embeddableLinkIfVisible() {
      if (this.showLinkPreview) {
        return this.embeddableLink
      }
      return 'about:blank'
    },
    isDone() {
      return get(this, 'taskRecordReview.status') === 'DONE'
    },
    isPending() {
      return get(this, 'taskRecordReview.status') === 'PENDING'
    },
    classList() {
      return {
        'task-record-review-card--active': this.active,
        'task-record-review-card--selected': this.selected,
        'task-record-review-card--done': this.isDone,
        'task-record-review-card--pending': this.isPending
      }
    },
    loader() {
      return uniqueId('loader-task-record-review-')
    },
    overlayVariant() {
      if (this.taskRecordReview.status === 'DONE') {
        return 'lighter'
      }
      return 'white'
    }
  }
}
</script>

<template>
  <b-overlay :show="isLoading" :variant="overlayVariant" rounded="lg">
    <b-spinner variant="light" slot="overlay"/>
    <div :class="classList" class="task-record-review-card card card-body p-4 container-fluid">
      <div class="row no-gutters">
        <div class="col flex-grow-1">
          <div class="row no-gutters">
            <div class="col-lg-4">
              <div class="row no-gutters">
                <div class="task-record-review-card__id col-2 font-weight-bold text-nowrap">
                  <b-form-checkbox class="task-record-review-card__id__checkbox" v-model="selectedInput">
                    {{ taskRecord.id }}
                  </b-form-checkbox>
                </div>
                <div class="col text-center px-0 pb-3 text-lg-left">
                  <haptic-copy
                    :text="taskRecord.originalValue"
                    class="task-record-review-card__original-value font-weight-bold px-3 py-2"
                    tooltip-placement="right"
                    v-b-tooltip.hover.right="'Click to copy'">
                    {{ taskRecord.originalValue }}
                    <span class="task-record-review-card__original-value__clipboard ml-1">
                      <clipboard-icon/>
                    </span>
                  </haptic-copy>
                  <b-btn variant="link" class="text-muted px-3" :href="link" v-if="link" target="_blank">
                    <link-icon size="1x" class="mr-1"/>
                    Open link
                    <span v-if="active">
                      <shortkey-badge :value="['Ctrl', 'l']" class="ml-2"/>
                    </span>
                  </b-btn>
                </div>
                <div class="task-record-review-card__predicted-value col-3 font-weight-bold py-3 text-center">
                  {{ taskRecord.predictedValue }}
                </div>
              </div>
            </div>
            <div class="col-lg-8">
              <div class="row">
                <div class="col-12 col-xxl-6 pr-xxl-0">
                  <task-record-review-choice-form
                    class="task-record-review-card__choice"
                    :task-record-review-id="taskRecordReviewId"
                    :activate-shortkeys="active"
                    @submit="selectChoiceWithLoader"/>
                </div>
                <div class="col-12 col-xxl-6">
                  <task-record-review-history
                    class="task-record-review-card__history"
                    :task-record-review-id="taskRecordReviewId"
                    @toggle-notes="highlightAndToggleNotes($event)"
                    @same="selectChoiceWithLoader"
                    @cancel="selectChoiceWithLoader"/>
                </div>
              </div>
            </div>
          </div>
          <div class="row no-gutters">
            <div class="offset-4 col-8 col-xxl-4">
              <b-collapse :visible="showChanges">
                <task-record-changes
                  :action-ids="actionIds"
                  :activate-shortkeys="active"
                  @close="toggleChanges(false)"/>
              </b-collapse>
              <b-collapse :visible="showNotes">
                <task-record-review-notes
                  :task-record-review-id="taskRecordReviewId"
                  :activate-shortkeys="active"
                  :highlighted-review-id="highlightedReviewId"
                  @close="toggleNotes(false)"/>
              </b-collapse>
              <b-collapse :visible="showLinkPreview">
                <iframe
                  :src="embeddableLinkIfVisible"
                  class="border"
                  style="border:0"
                  loading="lazy"
                  allowfullscreen
                  width="100%"
                  height="400px"/>
              </b-collapse>
            </div>
          </div>
        </div>
        <div class="col-auto ml-3">
          <task-record-review-actions
            class="task-record-review-card__actions"
            :task-record-review-id="taskRecordReviewId"
            @lock="lockWithLoader"
            @unlock="unlockWithLoader"
            @toggle-changes="fetchAndToggleChanges()"
            @bookmark="bookmark"
            @unbookmark="unbookmark"/>
        </div>
      </div>
    </div>
  </b-overlay>
</template>

<style lang="scss" scoped>
.task-record-review-card {
  box-shadow: $box-shadow-sm;

  &--active, &--selected {
    border: 1px solid $primary;
    box-shadow: $box-shadow-sm;
  }

  &--active {
    box-shadow: $box-shadow-lg;
  }

  &--done {
    background: $lighter;
  }

  &__id {
    text-align: center;
    overflow: hidden;
    width: 100px;

    &__checkbox {
      padding: 0;

      & ::v-deep label {
        width: 100%;
        padding: $spacer 0;
      }

      & ::v-deep label:before,
      & ::v-deep label:after {
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
      }
    }

    &:hover &__checkbox ::v-deep label,
    .task-record-review-card--selected & &__checkbox ::v-deep label {
      text-indent: -1000px;

      &:after, &:before {
        display: block;
      }
    }

    &__checkbox ::v-deep label {
      text-indent: 0px;

      &:after, &:before {
        display: none;
      }
    }
  }

  &__original-value {
    text-align: inherit;
    display: flex;

    &:hover {
      background: $primary-10;
    }

    &__clipboard {
      min-width: 1.2rem;
      align-self: center;
      color: $tertiary;
      opacity: 0;
      transition: $btn-transition, opacity .15s;
    }

    &:hover &__clipboard {
      opacity: 1;
    }
  }

  @include media-breakpoint-down(xxl) {
    &__choice {
      margin-bottom: $spacer;
    }
  }

  &__actions {
    min-width: 0;
    opacity: 0.25;
  }

  &:hover &__actions,
  &--active &__actions {
    opacity: 1;
  }

}
</style>
