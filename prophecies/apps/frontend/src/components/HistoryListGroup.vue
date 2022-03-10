<script>
import { uniqueId } from 'lodash'
import Action from '@/models/Action'
import HistoryListItem, { ITEM_TYPES } from '@/components/HistoryListItem.vue'
import Task from '@/models/Task'
import User from '@/models/User'

export default {
  name: 'HistoryListGroup',
  components: {
    HistoryListItem
  },
  props: {
    limit: {
      type: Number,
      default: -1
    },
    fluid: {
      type: Boolean,
      default: true
    },
    actionIds: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      more: 5,
      nbTimesMore: 0,
      checkedRecords: []
    }
  },
  methods: {
    loadMore () {
      this.nbTimesMore++
    },
    sortByTimestamp (a, b) {
      return -a.timestamp.localeCompare(b.timestamp)
    },
    countCheckedReviewsByDateUserIdTaskId (acc, checkedItem) { // compute checked reviews (reviewed - cancelled)
      const date = new Date(checkedItem.date).toISOString()
      const id = `${date}_${checkedItem.userId}_${checkedItem.taskId}`
      const count = checkedItem.verb === 'reviewed' ? checkedItem.count : -checkedItem.count
      if (!acc[id]) {
        const currentTask = Task.query().with('project').find(checkedItem.taskId)
        acc[id] = {
          type: ITEM_TYPES.CHECKED_RECORDS,
          timestamp: date,
          user: User.query().find(checkedItem.userId),
          content: 0,
          projectName: currentTask.project?.name,
          taskName: currentTask.name,
          link: `#/task-record-reviews/${checkedItem.taskId}`
        }
      }
      acc[id].content += count

      if (acc[id].content === 0) {
        delete acc[id]
      }

      return acc
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('load-history-item-')
    },
    closedTasks () {
      return Action
        .query()
        .with('actor')
        .with('target')
        .with('target.name')
        .with('target.project')
        .whereIdIn(this.actionIds)
        .where('targetType', 'Task')
        .where('verb', 'closed')
        .get()
        .map(task => ({
          type: ITEM_TYPES.CLOSED_TASK,
          timestamp: task.timestamp,
          user: task.actor,
          projectName: task.target.project?.name,
          taskName: task.target.name
        }))
    },
    mentions () {
      return Action
        .query()
        .with('actor')
        .with('target')
        .with('actionObject')
        .with('actionObject.task')
        .with('actionObject.task.project')
        .whereIdIn(this.actionIds)
        .where('verb', 'mentioned')
        .get()
        .map(mention => ({
          type: ITEM_TYPES.MENTIONED_USER,
          timestamp: mention.timestamp,
          user: mention.actor,
          content: mention.target,
          projectName: mention.actionObject.task?.project?.name,
          taskName: mention.actionObject.task?.name,
          link: mention.link
        }))
    },
    tips () {
      return Action
        .query()
        .with('actor')
        .with('target')
        .with('target.task')
        .with('target.project')
        .whereIdIn(this.actionIds)
        .where('targetType', 'Tip')
        .where('verb', 'created')
        .get()
        .map(tip => ({
          type: ITEM_TYPES.TIP,
          timestamp: tip.target.createdAt,
          user: tip.actor,
          content: tip.target.name,
          projectName: tip.target.project?.name,
          taskName: tip.target.task?.name,
          link: `#/tips/${tip.target.id}`
        }))
    },
    reviewedOrCancelledItems () {
      return Action
        .query()
        .with('actor')
        .with('target')
        .with('target.task')
        .with('target.task.project')
        .whereIdIn(this.actionIds)
        .where('targetType', 'ActionAggregate')
        .where('verb', 'created-aggregate')
        .get()
        .reduce((prev, action) => {
          if (action.target.verb === 'reviewed' || action.target.verb === 'cancelled') {
            prev.push(action.target)
          }
          return prev
        }, [])
    },
    reviewedItems () {
      return Object.values(this.reviewedOrCancelledItems.reduce(this.countCheckedReviewsByDateUserIdTaskId, {}))
    },

    items () {
      return [...this.mentions,
        ...this.closedTasks,
        ...this.tips,
        ...this.reviewedItems]
        .map((item, i) => { return { ...item, id: `history-item-${i}` } })
    },
    sortedByTimestampItems () {
      return this.items.slice().sort(this.sortByTimestamp)
    },
    nbVisibleItems () {
      const limitAndMore = this.limit + this.more * this.nbTimesMore
      return this.limit > 0 ? limitAndMore : this.sortedByTimestampItems.length
    },
    nbTotalItems () {
      return this.sortedByTimestampItems.length
    },
    hasMoreToSee () {
      return this.nbVisibleItems < this.nbTotalItems
    },
    visibleItems () {
      return this.sortedByTimestampItems.slice(0, this.nbVisibleItems)
    },
    isFluidClass () {
      return this.fluid ? 'container-fluid' : 'container'
    }
  }
}
</script>

<template>
  <div v-if="visibleItems.length" class="history-list-group px-0 history-list-group" :class="isFluidClass">
    <ul class="history-list-group__list list-unstyled pb-3">
        <history-list-item v-for="(item) in visibleItems" :key="item.id" :id="item.id"
        :project-name="item.projectName"
        :task-name="item.taskName"
        :link="item.link"
        :timestamp="item.timestamp"
        :type="item.type"
        :creator="item.user"
        :value="item.content"
        />
    </ul>

    <slot name="footer">
      <div class="history-list-group__see-more d-flex justify-content-center py-3" v-if="hasMoreToSee">
        <button class="history-list-group__see-more__button btn btn-primary border font-weight-bold text-white" @click='loadMore'>
        {{$t('historyListGroup.seeMore')}}
        </button>
      </div>
    </slot>
  </div>
</template>
