<script>
import User from '@/models/User'
import Task from '@/models/Task'
import Project from '@/models/Project'
import Tip from '@/models/Tip'
import moment from 'moment'

export const ITEM_TYPES = {
  TIP: 'tip',
  CHECKED_RECORDS: 'checked-records',
  CLOSED_TASK: 'closed-task',
  MENTIONED_USER: 'mentioned-user'
}

const ITEM_TYPES_CONTENT = {
  [ITEM_TYPES.TIP]: { prefix: '<span class="history-list-item__prefix history-list-item__prefix__tip"></span>', text: 'added a new tip' },
  [ITEM_TYPES.CHECKED_RECORDS]: { prefix: '<span class="history-list-item__prefix "></span>', text: 'checked $value records' },
  [ITEM_TYPES.CLOSED_TASK]: { prefix: '<span class="history-list-item__closed-task-prefix">🎉</span>', text: 'closed the task' },
  [ITEM_TYPES.MENTIONED_USER]: { prefix: '<span class="history-list-item__prefix history-list-item__prefix__mention"></span>', text: 'mentioned $value in a note' }
}

export default {
  name: 'HistoryListItem',
  props: {
    type: {
      type: String,
      required: true
    },
    projectName: {
      type: String,
      default: null
    },
    taskName: {
      type: String,
      default: null
    },
    link: {
      type: String,
      default: null
    },
    creator: {
      type: Object,
      required: true
    },
    timestamp: {
      type: String,
      required: true
    },
    value: {
      type: [String, Object],
      default: null
    }
  },
  filters: {
    formatDate (d) {
      return moment(d).format('ddd DD, MMM YYYY - h:MMa')
    }
  },
  methods: {
    task (taskId) {
      return Task
        .query()
        .find(taskId).get()
    },
    project (projectId) {
      return Project
        .query()
        .find(projectId).get()
    },
    tip (tipId) {
      return Tip
        .query()
        .find(tipId).get()
    },
    user (userId) {
      return User
        .query()
        .find(userId).get()
    },
    userDisplayName (user, capitalize = false) {
      if (user.isMe) {
        return capitalize ? 'You' : 'you'
      }
      if (!user.firstName || !user.lastName) {
        return user.username
      }
      return `${user.firstName}`
    },
    mentionContent (user) {
      return `${this.userDisplayName(user)} (@${user.username})`
    }
  },
  computed: {
    prefix () {
      return ITEM_TYPES_CONTENT[this.type].prefix
    },
    className () {
      return this.type === ITEM_TYPES.CHECKED_RECORDS ? '' : 'font-weight-bold'
    },
    category () {
      let category = 'General'
      if (this.projectName) {
        category = this.projectName
        const taskName = this.taskName ?? 'General'
        category = taskName + ' | ' + category
      }
      return category
    },
    content () {
      const content = ITEM_TYPES_CONTENT[this.type]
      const text = content.text
      let itemText = text
      switch (this.type) {
        case ITEM_TYPES.CHECKED_RECORDS:
        {
          itemText = text.replace('$value', this.value)
          break
        }
        case ITEM_TYPES.MENTIONED_USER:
        {
          itemText = text.replace('$value', this.mentionContent(this.value))
          break
        }
        case ITEM_TYPES.TIP:
        {
          itemText = `${text}: "${this.value}"`
          break
        }
      }
      return itemText
    },
    hasLink () {
      return this.type === ITEM_TYPES.MENTIONED_USER || this.type === ITEM_TYPES.TIP
    },
    who () {
      return this.userDisplayName(this.creator, true)
    }
  }
}
</script>

<template>
  <li class="history-list-item row py-3 m-0">
    <div  class="history-list-item__prefix-column" v-html="prefix"></div>
    <div class="row container-fluid justify-content-between flex-grow-1">
        <div class="d-flex flex-grow-lg-0 flex-grow-1 px-3 py-1 history-list-item__content-column col-12 col-lg-5" :class="className">
          <p>{{who }}<a v-if="hasLink" class="pl-1" :href='`${link}`'> {{content}} </a> <template v-else> {{content}} </template></p>
        </div>
        <div class="d-flex ml-auto flex-md-row flex-lg-grow-0 justify-content-md-right flex-sm-column flex-sm-grow-1 justify-content-sm-between">
          <div class="px-3 py-1 text-sm-left text-lg-right history-list-item__category-column">{{category}}</div>

          <div class="ml-3  py-1 text-sm-left text-md-right  history-list-item__date-column">{{timestamp | formatDate}}</div>
        </div>
      </div>
  </li>
</template>

<style lang="scss">

 .history-list-item {
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
        min-width: 382px;
    }

    &__date-column {
      color: $secondary;
      min-width: 220px;
      width: 220px;
    }
 }
</style>
