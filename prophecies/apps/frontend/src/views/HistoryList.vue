<script>
import { uniqueId } from 'lodash'
import moment from 'moment'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'

const itemTypes = {
  tip: 'tip',
  checkedRecords: 'checked-records',
  closedTask: 'closed-task',
  mentionedUser: 'mentioned-user'
}

const itemTypesContent = {
  [itemTypes.tip]: { prefix: 'Tip', text: 'added a new tip' },
  [itemTypes.checkedRecords]: { prefix: 'Checked', key: 'nbRecords', text: 'checked $nbRecords records' },
  [itemTypes.closedTask]: { prefix: 'Closed', text: 'closed the task' },
  [itemTypes.mentionedUser]: { prefix: 'Mentioned', key: 'who', text: 'mentionned $who in a note' }
}

const pontus = { projectId: '1', projectName: 'Pontus', tasks: [{ taskId: '2', taskName: 'Passports' }] }
const chronos = { projectId: '2', projectName: 'Chronos', tasks: [{ taskId: '1', taskName: 'Addresses' }] }
const hemera = { projectId: '3', projectName: 'Hemera', tasks: [{ taskId: '3', taskName: 'SAR Extraction' }] }

const historyItems = [
  {
    type: itemTypes.tip,
    date: '2021-09-21T11:43:15.263Z',
    user: 'Emilia',
    content: 'How should I decide between “the BVI” and “BVI”?'
  },
  {
    type: itemTypes.checkedRecords,
    date: '2021-09-20T11:43:15.263Z',
    user: 'Jelena',
    nbRecords: 252,
    projectName: chronos.projectName,
    taskName: chronos.tasks[0].taskName
  },
  {
    type: itemTypes.closedTask,
    date: '2021-09-19T11:43:15.263Z',
    user: 'Delphine',
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
  },
  {
    type: itemTypes.mentionedUser,
    date: '2021-09-17T15:43:15.263Z',
    user: 'Delphine',
    who: 'Caroline',
    projectName: hemera.projectName,
    taskName: hemera.tasks[0].taskName
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
      historyItems: historyItems
    }
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchHistoryLoader, this.fetchHistory)
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
    async fetchHistory () {
      const { response } = await new Promise(() => historyItems)
      console.log(response)
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
      }
      return itemText
    },
    itemCategory (item) {
      if (item.type === itemTypes.tip) {
        return 'General'
      } else {
        return `${item.taskName} | ${item.projectName}`
      }
    },
    itemPrefix (item) {
      return itemTypesContent[item.type].prefix
    },
    formatItemDate (d) {
      return moment(d).format('ddd DD, MMM YYYY - h:MMa')
      // return moment(d).format('lll')
    }
  },
  computed: {

    fetchHistoryLoader () {
      return uniqueId('load-history-item-')
    }
  }
}
</script>

<template>
  <div class="history-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="tip-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <h1 class="font-weight-bold title">What happened <span class="">lately</span></h1>
        <app-waiter :loader="fetchHistoryLoader" waiter-class="my-5 mx-auto d-block">
          <div v-if="historyItems">
            <ul class="list-unstyled row  ">
              <li v-for="(item,i) in historyItems" :key="i" class="row container">
                <div class="col-1">{{itemPrefix(item)}}</div>
                <div class="col-6 ">{{item.user}}
                {{itemTypeContent(item)}}</div>
                <div class="col-3 text-right">{{itemCategory(item)}}</div>
                <div class="col-2 text-justify">{{formatItemDate(item.date)}}</div>
              </li>
            </ul>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
 .history-list {
   color:"blue"
 }
</style>
