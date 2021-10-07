<script>
import { uniqueId } from 'lodash'
import moment from 'moment'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
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
  [itemTypes.tip]: { prefix: '<span class="history__prefix history__prefix__tip"></span>', text: 'added a new tip' },
  [itemTypes.checkedRecords]: { prefix: '<span class="history__prefix "></span>', key: 'nbRecords', text: 'checked $nbRecords records' },
  [itemTypes.closedTask]: { prefix: '<span class="history__closed-task-prefix">🎉</span>', text: 'closed the task' },
  [itemTypes.mentionedUser]: { prefix: '<span class="history__prefix history__prefix__mention"></span>', key: 'who', text: 'mentioned $who in a note' }
}

const pontus = { projectId: '1', projectName: 'Pontus', tasks: [{ taskId: '2', taskName: 'Passports' }] }
const chronos = { projectId: '2', projectName: 'Chronos', tasks: [{ taskId: '1', taskName: 'Addresses' }] }

const historyItems = [

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
  name: 'History',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter
  },
  data () {
    return {
      historyItems: []
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
      this.historyItems = historyItems
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
    }
  },
  computed: {
    fetchHistoryLoader () {
      return uniqueId('load-history-item-')
    },
    fetchActionLoader () {
      return uniqueId('load-actions-item-')
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
      return this.historyItems.slice()
    },
    items () {
      return [...this.mentions, ...this.closedTasks, ...this.tips, ...this.aggregatedItems]
        .sort((a, b) => -a.date.localeCompare(b.date))
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
    }
  }
}
</script>

<template>
  <div class="history d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="history__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <h1 class="font-weight-bold mb-5 history__title">What happened <span class="history__title--lately">lately</span></h1>
        <app-waiter :loader="fetchHistoryLoader" waiter-class="my-5 mx-auto d-block">
          <div v-if="historyItems">
            <ul class="list-unstyled ">
              <li v-for="(item,i) in items" :key="i" class="row container-fluid py-3">
                <div  class="history__prefix-column" v-html="item.prefix"></div>
                <div class="col-12 row">
                  <div class="col-xs-12 col-lg-6" :class="item.class">{{item.user}} {{item.content}}</div>
                  <div class="col-xs-5 col-lg-3 text-right history__category-column">{{item.category}}</div>
                  <div class="col-xs-7 col-lg-3 text-right history__date-column">{{item.date}}</div>
                </div>
              </li>
            </ul>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
 .history {
    &__title{
      color:$primary;
      &--lately{
        color:$danger;
      }
    }
    &__prefix-column{
      width:15px;
      text-align: center;
    }
    &__category-column {
      min-width: 220px;
    }
    &__date-column {
      color: $secondary;
      min-width: 220px;
    }
    & /deep/ &__prefix{
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
 }
</style>
