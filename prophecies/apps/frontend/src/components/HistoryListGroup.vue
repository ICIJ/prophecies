<script>
import { uniqueId } from 'lodash'
import Action from '@/models/Action'
import Tip from '@/models/Tip'
import HistoryListItem, { ITEM_TYPES } from '@/components/HistoryListItem.vue'
import Task from '@/models/Task'
import User from '@/models/User'
import ActionAggregate from '@/models/ActionAggregate'

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
    task (taskId) {
      return Task
        .query()
        .find(taskId)
        .with('project')
        .get()
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
        .where('targetType', 'Task')
        .where('verb', 'closed')
        .get()
        .map(task => {
          return {
            type: ITEM_TYPES.CLOSED_TASK,
            timestamp: task.timestamp,
            user: task.actor,
            projectName: task.target.project?.name,
            taskName: task.target.name
          }
        })
    },
    mentions () {
      return Action
        .query()
        .with('actor')
        .with('target')
        .with('actionObject')
        .with('actionObject.task')
        .with('actionObject.task.project')
        .where('verb', 'mentioned')
        .get()
        .map(mention => {
          return {
            type: ITEM_TYPES.MENTIONED_USER,
            timestamp: mention.timestamp,
            user: mention.actor,
            content: mention.target,
            projectName: mention.actionObject.task?.project?.name,
            taskName: mention.actionObject.task?.name,
            link: mention.link
          }
        })
    },
    tips () {
      return Tip
        .query()
        .with('task')
        .with('project')
        .with('creator')
        .get()
        .map(tip => {
          return {
            type: ITEM_TYPES.TIP,
            timestamp: tip.createdAt,
            user: tip.creator,
            content: tip.name,
            projectName: tip.project?.name,
            taskName: tip.task?.name,
            link: `#/tips/${tip.id}`
          }
        })
    },
    aggregatedItems () {
      const agg = ActionAggregate
        .query()
        .get()
      const users = {}
      const tasks = {}
      return agg.map(checkedItem => {
        if (!tasks[checkedItem.taskId]) {
          tasks[checkedItem.taskId] = Task.query().with('project').find(checkedItem.taskId)
        }
        if (!users[checkedItem.userId]) {
          users[checkedItem.userId] = User.query().find(checkedItem.userId)
        }
        return {
          type: ITEM_TYPES.CHECKED_RECORDS,
          timestamp: new Date(checkedItem.date).toISOString(),
          user: users[checkedItem.userId],
          content: checkedItem.count,
          projectName: tasks[checkedItem.taskId].project?.name,
          taskName: tasks[checkedItem.taskId].name,
          link: `#/task-record-reviews/${checkedItem.taskId}`
        }
      })
    },

    items () {
      let key = 0
      return [...this.mentions,
        ...this.closedTasks,
        ...this.tips,
        ...this.aggregatedItems]
        .map((item, i) => { return { ...item, id: `history-item-${++key}` } })
    },
    sortedByTimestampItems () {
      return this.items.slice().sort((a, b) => -a.timestamp.localeCompare(b.timestamp))
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
        See more
        </button>
      </div>
    </slot>
  </div>
</template>
