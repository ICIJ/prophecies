<script>
import { get, uniqueId } from 'lodash'
import TaskRecordReviewActions from '@/components/TaskRecordReviewActions'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'
import TaskRecordReviewHistory from '@/components/TaskRecordReviewHistory'
import TaskRecordReviewNotes from '@/components/TaskRecordReviewNotes'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordReview from '@/models/TaskRecordReview'

export default {
  name: 'TaskRecordReviewCard',
  components: {
    TaskRecordReviewActions,
    TaskRecordReviewChoiceForm,
    TaskRecordReviewHistory,
    TaskRecordReviewNotes
  },
  data () {
    return {
      showNotes: false
    }
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
    }
  },
  methods: {
    async selectChoiceWithLoader (data) {
      this.$wait.start(this.updateLoader)
      await this.selectChoice(data)
      this.$wait.end(this.updateLoader)
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
      this.$wait.start(this.updateLoader)
      await this.lock()
      this.$wait.end(this.updateLoader)
    },
    async unlock () {
      await TaskRecord.api().unlock(this.taskRecord.id)
      // Let parent component know about the update
      this.emitUpdate()
    },
    async unlockWithLoader () {
      this.$wait.start(this.updateLoader)
      await this.unlock()
      this.$wait.end(this.updateLoader)
    },
    toggleNotes () {
      this.showNotes = !this.showNotes
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
      return this.taskRecordReview.taskRecord
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
    updateLoader () {
      return uniqueId('update-task-record-review-')
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
  <b-overlay :show="$wait.is(updateLoader)" :variant="overlayVariant" rounded="lg">
    <b-spinner variant="light" slot="overlay" />
    <div class="task-record-review-card card card-body p-4" :class="classList">
      <div class="row align-items-center">
        <div class="task-record-review-card__id col-1 col-lg-auto font-weight-bold text-nowrap">
          <b-form-checkbox class="task-record-review-card__id__checkbox" v-model="selectedInput">
            {{ taskRecordReview.taskRecord.id }}
          </b-form-checkbox>
        </div>
        <div class="task-record-review-card__original-value col-8 col-lg-3 font-weight-bold py-3 text-center text-lg-left">
          {{ taskRecordReview.taskRecord.originalValue }}
        </div>
        <div class="task-record-review-card__original-value col-3 col-lg-1 font-weight-bold py-3 text-center text-lg-left">
          {{ taskRecordReview.taskRecord.predictedValue }}
        </div>
        <div class="task-record-review-card__choice col">
          <div class="row align-items-center">
            <div class="task-record-review-card__choice__form col-xl-6">
              <task-record-review-choice-form @submit="selectChoiceWithLoader" :task-record-review-id="taskRecordReviewId" :activate-shortkeys="active" />
            </div>
            <div class="task-record-review-card__choice_history col-xl-6">
              <task-record-review-history :task-record-review-id="taskRecordReviewId" @toggle-notes="toggleNotes" />
            </div>
          </div>
        </div>
        <div class="task-record-review-card__actions col-auto">
          <task-record-review-actions :task-record-review-id="taskRecordReviewId"
            @lock="lockWithLoader"
            @unlock="unlockWithLoader" />
        </div>
      </div>
      <b-collapse :visible="showNotes">
        <task-record-review-notes :task-record-review-id="taskRecordReviewId" :autofocus="showNotes" @close="toggleNotes" />
      </b-collapse>
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
