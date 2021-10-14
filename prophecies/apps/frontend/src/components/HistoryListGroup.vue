<script>
import { uniqueId } from 'lodash'
import Action from '@/models/Action'
import Tip from '@/models/Tip'
import User from '@/models/User'
import HistoryListItem, { ITEM_TYPES } from '@/components/HistoryListItem.vue'

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
    isMe ({ id = null } = {}) {
      return id === User.me().id
    },
    userDisplayName (user, capitalize = false) {
      if (this.isMe(user)) {
        return capitalize ? 'You' : 'you'
      }
      if (!user.firstName || !user.lastName) {
        return user.username
      }
      return `${user.firstName}`
    },
    loadMore () {
      this.nbTimesMore++
    },
    mentionContent (user) {
      return `${this.userDisplayName(user)} (@${user.username})`
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
            date: task.timestamp,
            user: this.userDisplayName(task.actor, true),
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
            date: mention.timestamp,
            user: this.userDisplayName(mention.actor, true),
            content: this.mentionContent(mention.target),
            objectId: mention.actionObject.id,
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
            date: tip.createdAt,
            user: this.userDisplayName(tip.creator, true),
            content: tip.name,
            objectId: tip.id,
            projectName: tip.project?.name,
            taskName: tip.task?.name,
            link: `#/tips/${tip.id}`
          }
        })
    },
    aggregatedItems () {
      return this.checkedRecords.slice()
    },
    unorderedItems () {
      return [...this.mentions, ...this.closedTasks, ...this.tips, ...this.aggregatedItems]
        .sort((a, b) => -a.date.localeCompare(b.date))
    },
    nbVisibleItems () {
      const limitAndMore = this.limit + this.more * this.nbTimesMore
      return this.limit > 0 ? limitAndMore : this.unorderedItems.length
    },
    nbTotalItems () {
      return this.unorderedItems.length
    },
    hasMoreToSee () {
      return this.nbVisibleItems < this.nbTotalItems
    },
    items () {
      return this.unorderedItems.slice(0, this.nbVisibleItems)
    },
    isFluidClass () {
      return this.fluid ? 'container-fluid' : 'container'
    }
  }
}
</script>

<template>
  <div v-if="items.length" class="px-0 history-list-group" :class="isFluidClass">
    <ul class="list-unstyled pb-3">
        <history-list-item v-for="(item,i) in items" :key="i"
        :project-name="item.projectName"
        :id="item.objectId"
        :task-name="item.taskName"
        :link="item.link"
        :timestamp="item.date"
        :type="item.type"
        :who="item.user"
        :value="item.content"
        />
    </ul>

    <slot name="footer">
      <div class="d-flex justify-content-center py-3" v-if="hasMoreToSee">
        <button class="btn btn-primary border font-weight-bold text-white" @click='loadMore'>
        See more
        </button>
      </div>
    </slot>
  </div>
</template>
