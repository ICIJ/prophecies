<script>
import { get, map, uniqueId } from 'lodash'
import TaskRecordChanges from '@/components/TaskRecordChanges'
import TaskRecordReviewActions from '@/components/TaskRecordReviewActions'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'
import TaskRecordReviewHistory from '@/components/TaskRecordReviewHistory'
import TaskRecordReviewNotes from '@/components/TaskRecordReviewNotes'
import Action from '@/models/Action'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCard',
  components: {
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
    highlightNote: {
      type: Boolean
    }
  },
  data () {
    return {
      showChanges: false,
      showNotes: false,
      highlightedReviewId: null,
      actionIds: []
    }
  },
  watch: {
    isLoading () {
      this.showChanges = false
      this.showNotes = false
      this.$root.$emit('bv::hide::tooltip')
    }
  },
  created () {
    this.toggleNotes(!!this.highlightNote, this.taskRecordReviewId)
  },
  methods: {
    async selectChoiceWithLoader (data) {
      this.$wait.start(this.loader)
      await this.selectChoice(data)
      this.$wait.end(this.loader)
    },
    async selectChoice (data) {
      // We use a dedicated method that will format the data for the JSONAPI spec
      // and return the updated object (the store shall be updated as well).
      await TaskRecordReview.api().selectChoice(this.taskRecordReviewId, data)
      // Hide node to avoid using unecessary space
      this.showNotes = false
      // Let parent component know about the update
      this.emitUpdate()
    },
    async lock () {
      await TaskRecord.api().lock(this.taskRecord.id)
      // Let parent component know about the update
      this.emitUpdate()
    },
    async lockWithLoader () {
      this.$wait.start(this.loader)
      await this.lock()
      this.$wait.end(this.loader)
    },
    async unlock () {
      await TaskRecord.api().unlock(this.taskRecord.id)
      // Let parent component know about the update
      this.emitUpdate()
    },
    async unlockWithLoader () {
      this.$wait.start(this.loader)
      await this.unlock()
      this.$wait.end(this.loader)
    },
    async fetchTaskRecordActions () {
      const taskRecordId = this.taskRecordReview.taskRecordId
      const { response } = await Action.api().forTaskRecord(taskRecordId)
      this.actionIds = get(response, 'data.data', []).map(a => a.id)
    },
    async fetchTaskRecordActionsWithLoader () {
      this.$wait.start(this.loader)
      await this.fetchTaskRecordActions()
      this.$wait.end(this.loader)
    },
    async toggleChanges (toggler = null) {
      if (!this.showChanges || toggler) {
        await this.fetchTaskRecordActionsWithLoader()
      }
      this.showChanges = toggler !== null ? !!toggler : !this.showChanges
    },
    toggleNotes (toggler = null, highlightedReviewId) {
      if (!this.showNotes || toggler) {
        this.showChanges = false
        this.highlightedReviewId = highlightedReviewId
      }
      this.showNotes = toggler !== null ? !!toggler : !this.showNotes
    },
    emitUpdate () {
      /**
       * Fired when the task record review is updated
       * @event update
       */
      this.$emit('update')
    }
  },
  computed: {
    isLoading () {
      return this.$wait.is(this.loader)
    },
    selectedInput: {
      get () {
        return this.selected
      },
      set (value) {
        return this.$emit('update:selected', value)
      }
    },
    taskRecordReview () {
      return TaskRecordReview
        .query()
        .with('taskRecord')
        .find(this.taskRecordReviewId)
    },
    taskRecord () {
      return get(this, 'taskRecordReview.taskRecord')
    },
    isDone () {
      return get(this, 'taskRecordReview.status') === 'DONE'
    },
    isPending () {
      return get(this, 'taskRecordReview.status') === 'PENDING'
    },
    classList () {
      return {
        'task-record-review-card--active': this.active,
        'task-record-review-card--selected': this.selected,
        'task-record-review-card--done': this.isDone,
        'task-record-review-card--pending': this.isPending,
      }
    },
    loader () {
      return uniqueId('loader-task-record-review-')
    },
    overlayVariant () {
      if (this.taskRecordReview.status === 'DONE') {
        return 'lighter'
      }
      return 'white'
    }
  }
}
</script>

<template>
  <b-overlay :show="$wait.is(loader)" :variant="overlayVariant" rounded="lg">
    <b-spinner variant="light" slot="overlay" />
    <div class="task-record-review-card card card-body p-4 container-fluid" :class="classList">
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
                <div class="task-record-review-card__original-value col font-weight-bold py-3 text-center text-lg-left">
                  {{ taskRecord.originalValue }}
                </div>
                <div class="task-record-review-card__original-value col-3 font-weight-bold py-3 text-center">
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
                    @submit="selectChoiceWithLoader" />
                </div>
                <div class="col-12 col-xxl-6">
                  <task-record-review-history
                    class="task-record-review-card__history"
                    :task-record-review-id="taskRecordReviewId"
                    @toggle-notes="toggleNotes(true, $event)"
                    @same="selectChoiceWithLoader" />
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
                  @close="toggleChanges(false)" />
              </b-collapse>
              <b-collapse :visible="showNotes">
                <task-record-review-notes
                  :task-record-review-id="taskRecordReviewId"
                  :activate-shortkeys="active"
                  :highlighted-review-id="highlightedReviewId"
                  @close="toggleNotes(false)" />
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
            @toggle-changes="toggleChanges()" />
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

        & /deep/ label {
          width: 100%;
          padding: $spacer 0;
        }

        & /deep/ label:before,
        & /deep/ label:after {
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }
      }

      &:hover &__checkbox /deep/ label,
      .task-record-review-card--selected & &__checkbox /deep/ label {
        text-indent: -1000px;

        &:after, &:before {
          display: block;
        }
      }

      &__checkbox /deep/ label {
        text-indent: 0px;

        &:after, &:before {
          display: none;
        }
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
