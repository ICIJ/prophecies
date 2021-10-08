<script>
import { uniqueId } from 'lodash'
import moment from 'moment'
import AppWaiter from '@/components/AppWaiter'
import Action from '@/models/Action'
import Task from '@/models/Task'
import Tip from '@/models/Tip'
import TaskRecordReview from '@/models/TaskRecordReview'

const itemTypes = {
  tip: 'tip',
  checkedRecords: 'checked-records',
  closedTask: 'closed-task',
  mentionedUser: 'mentioned-user'
}

const itemTypesContent = {
  [itemTypes.tip]: { prefix: '<span class="history-list__prefix history-list__prefix__tip"></span>', text: 'added a new tip' },
  [itemTypes.checkedRecords]: { prefix: '<span class="history-list__prefix "></span>', key: 'nbRecords', text: 'checked $nbRecords records' },
  [itemTypes.closedTask]: { prefix: '<span class="history-list__closed-task-prefix">🎉</span>', text: 'closed the task' },
  [itemTypes.mentionedUser]: { prefix: '<span class="history-list__prefix history-list__prefix__mention"></span>', key: 'who', text: 'mentioned $who in a note' }
}

const pontus = { projectId: '1', projectName: 'Pontus', tasks: [{ taskId: '2', taskName: 'Passports' }] }
const chronos = { projectId: '2', projectName: 'Chronos', tasks: [{ taskId: '1', taskName: 'Addresses' }] }

const checkedRecords = [

  {
    type: itemTypes.checkedRecords,
    date: '2021-09-20T11:43:15.263Z',
    user: 'Jelena',
    nbRecords: 252,
    projectName: chronos.projectName,
    taskName: chronos.tasks[0].taskName
  },

  {
    type: itemTypes.checkedRecords,
    date: '2021-09-19T11:43:15.263Z',
    user: 'Augie',
    nbRecords: 2,
    projectName: pontus.projectName,
    taskName: pontus.tasks[0].taskName
  }

]

export default {
  name: 'HistoryList',
  components: {
    AppWaiter
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
  async created () {
    await this.setup()
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchHistoryLoader, this.fetchAll)
      } catch (error) {
        const title = 'Unable to retrieve history'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    async fetchAll () {
      this.checkedRecords = checkedRecords
      await Task.api().get()
      await Action.api().get()
      await Tip.api().get()
    },
    fetchTasks () {
      return Task.api().get()
    },
    fetchTask (taskId) {
      const task = Task.find(taskId)
      if (!task) {
        return Task.api().find(taskId)
      }
      return task
    },
    fetchTaskRecordReview (taskRecordReviewId) {
      const taskRecordReview = TaskRecordReview.find(taskRecordReviewId)
      if (!taskRecordReview) {
        return TaskRecordReview.api().find(taskRecordReviewId)
      }
      return taskRecordReview
    },
    historyItemId () {
      return uniqueId('history-item-')
    },
    itemTypeContent (item) {
      const content = itemTypesContent[item.type]
      let itemText = content.text
      switch (item.type) {
        case itemTypes.checkedRecords:
        case itemTypes.mentionedUser:
        {
          itemText = content.text.replace(`$${content.key}`, item[content.key])
          break
        }
        case itemTypes.tip:
        {
          itemText = `${content.text}: "${item.content}"`
          break
        }
      }
      return itemText
    },
    itemCategory (item) {
      let category = 'General'
      if (item.projectName) {
        category = item.projectName
        const taskName = item.taskName ?? 'General'
        category = taskName + ' | ' + category
      }
      return category
    },
    itemPrefix (item) {
      return itemTypesContent[item.type].prefix
    },
    formatItemDate (d) {
      return moment(d).format('ddd DD, MMM YYYY - h:MMa')
    },
    getBoldDisplay (item) {
      return item.type === itemTypes.checkedRecords ? '' : 'font-weight-bold'
    },
    userDisplayName (user) {
      if (!user.firstName || !user.lastName) {
        return user.username
      }
      return `${user.firstName}`
    },
    loadMore () {
      this.nbTimesMore++
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
            type: itemTypes.closedTask,
            date: task.timestamp,
            user: this.userDisplayName(task.actor),
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
            type: itemTypes.mentionedUser,
            date: mention.timestamp,
            user: this.userDisplayName(mention.actor),
            who: this.userDisplayName(mention.target),
            projectName: mention.actionObject.task?.project?.name,
            taskName: mention.actionObject.task?.name
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
            type: itemTypes.tip,
            date: tip.createdAt,
            user: this.userDisplayName(tip.creator),
            content: tip.name,
            projectName: tip.project?.name,
            taskName: tip.task?.name
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
        .map(item => {
          return {
            prefix: this.itemPrefix(item),
            user: item.user,
            content: this.itemTypeContent(item),
            category: this.itemCategory(item),
            date: this.formatItemDate(item.date),
            class: this.getBoldDisplay(item)
          }
        })
    },
    isFluidClass () {
      return this.fluid ? 'container-fluid' : 'container'
    }
  }
}
</script>

<template>
    <app-waiter :loader="fetchHistoryLoader" waiter-class="my-5 mx-auto d-block">
    <h1 class="font-weight-bold mt-3 mb-5 history-list__title"><slot name="title">What happened <span class="text-danger">lately</span></slot></h1>
      <div v-if="items.length" class="px-0" :class="isFluidClass">
        <ul class="list-unstyled pb-3">
          <li v-for="(item,i) in items" :key="i" class="row container-fluid py-3">
            <div  class="history-list__prefix-column" v-html="item.prefix"></div>
            <div class="row container-fluid">
              <div class="d-flex flex-grow-1 px-3 history-list__content-column" :class="item.class">{{item.user}} {{item.content}}</div>
              <div class="d-flex ml-sm-0 ml-auto  justify-content-md-right  flex-sm-column flex-md-row">
                <div class="px-3  text-md-left text-lg-right history-list__category-column">{{item.category}}</div>
                <div class="px-3 text-sm-left text-md-right  history-list__date-column">{{item.date}}</div>
              </div>
            </div>
          </li>
        </ul>
        <slot name="footer">
          <div class="d-flex justify-content-center pt-3" v-if="hasMoreToSee">
            <button class="btn btn-primary border font-weight-bold text-white" @click='loadMore'>
            See more ...
            </button>
          </div>
        </slot>
      </div>
    </app-waiter>
</template>

<style lang="scss">

 .history-list {
    &__title{
      color:$primary;
        letter-spacing: -2px;
    }

    &__prefix {
      display:inline-block;
      width:1em;
      height:8px;

      &__tip{
        background-color: $warning;
      }

      &__mention{
        background-color: $danger;
      }
    }

    &__prefix-column{
      width:15px;
      text-align: center;
    }

    &__category-column {
      width: 210px;
        min-width: 210px;
    }
    &__content-column {
        width: 310px;
        min-width: 310px;
    }

    &__date-column {
      color: $secondary;
      min-width: 220px;
      width: 220px;
    }
 }
</style>
