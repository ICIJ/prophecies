<script>
import { formatDateLongAlt } from '@/utils/date'
import User from '@/models/User'
import Task from '@/models/Task'
import Project from '@/models/Project'
import Tip from '@/models/Tip'
import UserLink from '@/components/UserLink'

export const ITEM_TYPES = {
  TIP: 'tip',
  CHECKED_RECORDS: 'checked-records',
  CLOSED_TASK: 'closed-task',
  MENTIONED_USER: 'mentioned-user'
}

const ITEM_TYPES_CONTENT = {
  [ITEM_TYPES.TIP]: { prefix: '<span class="history-list-item__prefix history-list-item__prefix__tip"></span>' },
  [ITEM_TYPES.CHECKED_RECORDS]: { prefix: '<span class="history-list-item__prefix "></span>' },
  [ITEM_TYPES.CLOSED_TASK]: { prefix: '<span class="history-list-item__closed-task-prefix">🎉</span>' },
  [ITEM_TYPES.MENTIONED_USER]: { prefix: '<span class="history-list-item__prefix history-list-item__prefix__mention"></span>' }
}

export default {
  name: 'HistoryListItem',
  components: {
    UserLink
  },
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
      type: [Number, String, Object],
      default: null
    }
  },
  filters: {
    formatDate (d) {
      return formatDateLongAlt(d)
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
        return capitalize ? this.$t('historyListItem.youCapitalized') : this.$t('historyListItem.youLowercase')
      }
      return `${user.displayName}`
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
    generalCategory () {
      return this.$t('historyListItem.general')
    },
    category () {
      let category = this.generalCategory
      if (this.projectName) {
        category = this.projectName
        const taskName = this.taskName ?? this.generalCategory
        category = `${taskName} | ${category}`
      }
      return category
    },
    content () {
      return this.type === ITEM_TYPES.MENTIONED_USER ? this.mentionContent(this.value) : this.value
    },
    hasLink () {
      return this.type === ITEM_TYPES.MENTIONED_USER || this.type === ITEM_TYPES.TIP
    }
  }
}
</script>

<template>
  <li class="history-list-item row py-3 m-0">
    <div  class="history-list-item__prefix-column" v-html="prefix"></div>
    <div class="row container-fluid justify-content-between flex-grow-1">
        <div class="d-flex flex-grow-lg-0 flex-grow-1 px-3 py-1 history-list-item__content-column col-12 col-lg-5" :class="className">
          <p>
            <user-link class="text-truncate" :user-id="creator.id">{{ userDisplayName(creator,true) }}</user-link> <span v-if="hasLink" v-html="$t(`historyListItem.${type}`, { value:content,link:link } )"></span><template v-else>{{$tc(`historyListItem.${type}`, content)}} </template></p>
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
