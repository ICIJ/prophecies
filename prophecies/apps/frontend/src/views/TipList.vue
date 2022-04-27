<script>
import { remove, groupBy, uniqueId } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import TaskStatus from '@/components/TaskStatus'
import Tip from '@/models/Tip'
import TipCard from '@/components/TipCard'
import TipListPageParams from '@/components/TipListPageParams'
import { orderByProjectThenTask } from '@/utils/sort'
import { TaskStatusEnum } from '@/models/Task'

const FILTER_TYPES = {
  PROJECT: 'filter[project]',
  TASK: 'filter[task]',
  CREATOR: 'filter[creator]'
}

export default {
  name: 'Tips',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter,
    LatestTipsCard,
    TaskStatus,
    TipCard,
    TipListPageParams
  },
  props: {
    query: {
      type: Object,
      default: () => ({
        [FILTER_TYPES.PROJECT]: null,
        [FILTER_TYPES.TASK]: null,
        [FILTER_TYPES.CREATOR]: null
      })
    }
  },
  data () {
    return {
      showLatestTips: true,
      projectFilter: this.query[FILTER_TYPES.PROJECT],
      taskFilter: this.query[FILTER_TYPES.TASK],
      creatorFilter: this.query[FILTER_TYPES.CREATOR],
      tipIds: []
    }
  },
  created () {
    return this.setup()
  },
  computed: {
    fetchTipsLoader () {
      return uniqueId('load-tips-')
    },
    fetchFilteredTipsLoader () {
      return uniqueId('load-filtered-tips-')
    },
    latestTips () {
      return Tip.query()
        .with('project')
        .with('task')
        .orderBy('createdAt', 'desc')
        .get()
    },
    tips () {
      return Tip.query()
        .with('project')
        .with('task')
        .get()
    },
    tasks () {
      return this.tips.reduce((tip, tasks) => {
        if (tip.task && !tasks[tip.task.id]) {
          tasks[tip.task.id] = tip.task
        }
        return tasks
      }, {})
    },
    projectId: {
      get () {
        return this.query[FILTER_TYPES.PROJECT]
      },
      set (value) {
        this.setProjectFilter(value)
      }
    },
    taskId: {
      get () {
        return this.query[FILTER_TYPES.TASK]
      },
      set (value) {
        this.setTaskFilter(value)
      }
    },
    creatorId: {
      get () {
        return this.query[FILTER_TYPES.CREATOR]
      },
      set (value) {
        this.setCreatorFilter(value)
      }
    },
    filteredTips () {
      const tips = this.tips.slice()
      if (this.query[FILTER_TYPES.PROJECT]) {
        remove(tips, t => t.projectId !== this.query[FILTER_TYPES.PROJECT])
      }
      if (this.query[FILTER_TYPES.TASK]) {
        remove(tips, t => t.taskId !== this.query[FILTER_TYPES.TASK])
      }
      if (this.query[FILTER_TYPES.CREATOR]) {
        remove(tips, t => t.creatorId !== this.query[FILTER_TYPES.CREATOR])
      }

      return orderByProjectThenTask(tips)
    },
    tipsGroupedByProjectThenTask () {
      const tipsGroupedByProject = groupBy(this.filteredTips, (tip) => {
        return tip.project ? tip.project.name : 'General'
      })
      for (const project in tipsGroupedByProject) {
        tipsGroupedByProject[project] = groupBy(tipsGroupedByProject[project], (tip) => {
          return tip.task ? tip.task.id : ''
        })
      }
      return tipsGroupedByProject
    },
    tipParams () {
      return {
        [FILTER_TYPES.PROJECT]: this.projectFilter,
        [FILTER_TYPES.TASK]: this.taskFilter,
        [FILTER_TYPES.CREATOR]: this.creatorFilter
      }
    }
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchTipsLoader, this.fetchTips)
      } catch (error) {
        const title = 'Unable to retrieve tips'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    fetchTips () {
      const include = 'project,task'
      const params = { include }
      return Tip.api().get('', { params })
    },
    taskClosed (taskId) {
      return this.tasks[taskId].status === TaskStatusEnum.CLOSED ?? false
    },
    setProjectFilter (val) {
      if (this.projectNotContainingTask(val, this.taskFilter)) {
        this.taskFilter = null
      }
      if (this.creatorFilter && this.projectNotContainingUser(val, this.creatorFilter)) {
        this.creatorFilter = null
      }
      this.projectFilter = val
      this.updateFilters()
    },
    setTaskFilter (val) {
      const tipsOfTask = Tip.query().where('taskId', val).get()
      // tipsOfTask can't be empty because it only uses taskId with at least a tip.
      // except when we remove the filter on tasks ...
      if (tipsOfTask[0].projectId) {
        this.projectFilter = tipsOfTask[0].projectId
      }
      if (this.creatorFilter && this.taskNotContainingUser(val, this.creatorFilter)) {
        this.creatorFilter = null
      }
      this.taskFilter = val
      this.updateFilters()
    },
    setCreatorFilter (val) {
      if (val !== null) {
        if (this.taskFilter && this.taskNotContainingUser(this.taskFilter, val)) {
          this.taskFilter = null
        }
        if (this.projectFilter && this.projectNotContainingUser(this.projectFilter, val)) {
          this.projectFilter = null
        }
      }
      this.creatorFilter = val
      this.updateFilters()
    },
    updateFilters () {
      return this.$router.push({ name: 'tip-list', query: this.tipParams })
    },
    projectNotContainingTask (projectId, taskId) {
      const tipsOfProject = Tip.query().where('projectId', projectId).get()
      return tipsOfProject.filter(t => t.taskId === taskId).length === 0
    },
    taskNotContainingUser (taskId, creatorId) {
      return Tip.query()
        .where('taskId', taskId)
        .where('creatorId', creatorId).get().length === 0
    },
    projectNotContainingUser (projectId, creatorId) {
      return Tip.query()
        .where('projectId', projectId)
        .where('creatorId', creatorId).get().length === 0
    }
  }
}
</script>

<template>
  <div class="tip-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="tip-list__container flex-grow-1">
      <app-header hide-nav />
      <div class="container-fluid px-4">
        <app-waiter :loader="fetchTipsLoader" waiter-class="my-5 mx-auto d-block">
          <b-collapse :visible="showLatestTips">
            <latest-tips-card :tips="latestTips" :show-close="true" @close="showLatestTips = false" class="mb-5">
              <template v-slot:title>
                <h1 class="latest-tips-card__title-tips text-primary mb-0 font-weight-bold">
                  Latest tips
                </h1>
              </template>
            </latest-tips-card>
          </b-collapse>
          <tip-list-page-params
            :project-id.sync="projectId"
            :task-id.sync="taskId"
            :creator-id.sync="creatorId"/>
          <div v-for="(tasksObject, projectName) in tipsGroupedByProjectThenTask" :key="projectName" class="tip-list__container__list my-4 border-bottom">
            <h1 class="mb-3 mt-4 text-primary">{{ projectName }}</h1>
            <div v-for="(taskTips, taskIdVal) in tasksObject" :key="taskIdVal" class="mb-4">
              <div class="d-flex flex-row my-4 ml-4">
                <template v-if="tasks[taskIdVal]">
                  <h2 class="text-tertiary">{{ tasks[taskIdVal].name }}</h2>
                  <task-status class="mt-0 ml-2" :task-id="taskIdVal" v-if="taskClosed(taskIdVal)" />
                </template>
              </div>
              <b-list-group-item v-for="tip in taskTips" class="flex-column align-items-start ml-4 border-0" :key="tip.id">
                <tip-card :tip-id="tip.id" />
              </b-list-group-item>
            </div>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
 .tip-list {
   .closed-indicator {
     margin-top: 2px;
     margin-left: 25px;
   }
 }
</style>
