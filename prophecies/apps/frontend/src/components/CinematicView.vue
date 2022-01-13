<script>
import TaskRecordReview from '@/models/TaskRecordReview'
import ShortkeyBadge from '@/components/ShortkeyBadge'
import TaskRecordReviewCard from '@/components/TaskRecordReviewCard'

export default {
  name: 'CinematicView',
  components: {
    ShortkeyBadge,
    TaskRecordReviewCard
  },
  props: {
    buzy: {
      type: Boolean
    },
    taskRecordReviewIds: {
      type: Array,
      default: () => ([])
    },
    pageNumber: {
      type: Number,
      default: 1
    },
    totalRows: {
      type: Number,
      default: 0
    },
    perPage: {
      type: Number,
      default: 10
    }
  },
  data () {
    return {
      id: null,
      idHistory: [],
      pageNumberHistory: [this.pageNumber],
      taskRecordReviewIdsPerPage: { [this.pageNumber]: this.taskRecordReviewIds }
    }
  }, 
  created () {
    this.id = this.defaultId
  },
  watch: {
    taskRecordReviewIds (ids) {
      this.$set(this.taskRecordReviewIdsPerPage, this.pageNumber, ids)
      this.id = this.defaultId
    },
    id (_, oldId = null) {
      this.idHistory.push(oldId)
    },
    pageNumber (_, oldPageNumber = null) {
      this.pageNumberHistory.push(oldPageNumber)
    }
  },
  computed: {
    taskRecordReviews () {
      return TaskRecordReview
        .query()
        .whereIdIn(this.taskRecordReviewIds)
    },
    pendingTaskRecordReviews () {
      return TaskRecordReview
        .query()
        .whereIdIn(this.taskRecordReviewIds)
        .where('status', 'PENDING')
        .where('locked', false)
    },
    availableTaskRecordReviews () {
      if (this.pendingTaskRecordReviews.exists()) {
        return this.pendingTaskRecordReviews
      }
      return this.taskRecordReviews
    },
    defaultTaskRecordReview () {
      if (this.pageNumberGoingBackward) {
        return this.availableTaskRecordReviews.last()
      }
      return this.availableTaskRecordReviews.first()
    },
    defaultId () {
      return this.defaultTaskRecordReview?.id || this.taskRecordReviewIds[0]
    },
    transition () {
      if (this.idGoingBackward) {
        return 'slide-backward'
      }
      return 'slide-forward'
    },
    idGoingBackward () {
      const ids = this.taskRecordReviewIdsHistory
      return ids.indexOf(this.id) < ids.indexOf(this.previousId)
    },
    pageNumberGoingBackward () {
      return this.pageNumber < this.previousPageNumber
    },
    previousId () {
      return this.idHistory.slice(-1).pop()
    },
    previousPageNumber () {
      return this.pageNumberHistory.slice(-1).pop()
    },
    isFirstPage () {
      return this.pageNumber === 1
    },
    isLastPage () {      
      return this.pageNumber === Math.ceil(this.totalRows / this.perPage)
    },
    hasPrevious () {
      return this.taskRecordReviewIds.indexOf(this.id) > 0 || !this.isFirstPage
    },
    hasNext () {
      return this.taskRecordReviewIds.indexOf(this.id) < this.taskRecordReviewIds.length - 1 || !this.isLastPage
    },
    progressIndex () {
      const isPageLoaded = this.pageNumber in this.taskRecordReviewIdsPerPage
      const currentPage = isPageLoaded ? this.pageNumber : this.previousPageNumber
      return (currentPage - 1) * this.perPage + this.taskRecordReviewIds.indexOf(this.id) + 1
    },
    taskRecordReviewIdsHistory () {
      return Object.values(this.taskRecordReviewIdsPerPage).flat()
    }
  },
  methods: {
    previous () {
      if (this.taskRecordReviewIds.indexOf(this.id) === 0 && !this.isFirstPage) {
        this.$delete(this.taskRecordReviewIdsPerPage, this.pageNumber - 1)  
        return this.$emit('previousPage')
      }
      const previous = this.taskRecordReviewIds.indexOf(this.id) - 1
      this.id = previous > -1 ? this.taskRecordReviewIds[previous] : this.id
    },
    next () {
      if (this.taskRecordReviewIds.indexOf(this.id) === this.taskRecordReviewIds.length - 1 && !this.isLastPage) {      
        this.$delete(this.taskRecordReviewIdsPerPage, this.pageNumber + 1)  
        return this.$emit('nextPage')
      }
      const next = this.taskRecordReviewIds.indexOf(this.id) + 1
      this.id = next > -1 ? this.taskRecordReviewIds[next] : this.id
    }
  }
}
</script>

<template>
  <div class="cinematic-view">
    <fieldset :disabled="buzy" class="cinematic-view__nav d-flex align-items-center justify-content-center text-center mb-3">
      <shortkey-badge :value="['Ctrl', '←']" class="mx-3" />
      <b-button @click="previous" 
                @shortkey="previous()"
                :disabled="!hasPrevious"
                v-shortkey="['ctrl', 'left']"
                variant="link"
                class="cinematic-view__nav__previous p-0">
        <ChevronLeftIcon size="3x" />
      </b-button>
      <div class="cinematic-view__nav__progress py-2 px-3 mx-4 rounded font-weight-bold d-flex align-items-center justify-content-center">
        <div class="mr-3">
          {{ progressIndex }}/{{ totalRows }}
        </div>
        <b-progress :value="progressIndex" 
                    :max="totalRows"
                    class="cinematic-view__nav__progress__bar"
                    show-progress 
                    variant="lighter" />
      </div>
      <b-button @click="next" 
                @shortkey="next()"
                :disabled="!hasNext"
                v-shortkey="['ctrl', 'right']"
                variant="link"
                class="cinematic-view__nav__next p-0">
        <ChevronRightIcon size="3x" />
      </b-button>
      <shortkey-badge :value="['Ctrl', '→']" class="mx-3" />
    </fieldset>
    <div class="position-relative">
      <transition :name="transition">
        <div class="cinematic-view__card" :key="id">
          <task-record-review-card 
            @update="next" 
            :task-record-review-id="id" 
            :frozen="buzy"
            active />
        </div>
      </transition>
    </div>
  </div>
</template>

<style lang="scss">
  .cinematic-view {

    &__nav {

      &__progress {
        background: $primary-70;
        color: #fff;
        min-width: 130px;

        &__bar {
          width: 25px;

          &.progress {
            height: 3px;

            &:after {
              top: 1px;
            }
          }
        }
      }
    }

    &__card {
      position: absolute;
      top: 0;
      left: 0; 
      right: 0; 
      z-index: 10;

      .task-record-review-card {
        border: 0;
      }
    }

    .slide-backward-enter-active, 
    .slide-backward-leave-active,
    .slide-forward-enter-active, 
    .slide-forward-leave-active {
      transition: transform .6s ease, opacity .6s ease;
    }

    .slide-forward-leave-to,
    .slide-backward-enter {
      opacity: 0;
      transform: translateX(-100%);
    }

    .slide-backward-leave-to,
    .slide-forward-enter {
      opacity: 0;
      transform: translateX(100%);
    }
  }
</style>