<script>
import { groupBy, uniqueId } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import Tip from '@/models/Tip'
import TipCard from '@/components/TipCard'
import TipListPageParams from '@/components/TipListPageParams'

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
      FILTER_TYPES: FILTER_TYPES,
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
    filteredTips () {
      let tips = this.tips.slice()
      if (this.query[FILTER_TYPES.PROJECT]) tips = tips.filter(t => t.projectId === this.query[FILTER_TYPES.PROJECT])
      if (this.query[FILTER_TYPES.TASK]) tips = tips.filter(t => t.taskId === this.query[FILTER_TYPES.TASK])
      if (this.query[FILTER_TYPES.CREATOR]) tips = tips.filter(t => t.creatorId === this.query[FILTER_TYPES.CREATOR])
      return tips
    },
    tipsGroupedByProject () {
      return groupBy(this.filteredTips, (tip) => {
        return tip.project ? tip.project.name : 'General'
      })
    },
    tipParams () {
      const filters = {}
      if (this.projectFilter) filters[FILTER_TYPES.PROJECT] = this.projectFilter
      if (this.taskFilter) filters[FILTER_TYPES.TASK] = this.taskFilter
      if (this.creatorFilter) filters[FILTER_TYPES.CREATOR] = this.creatorFilter
      return filters
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
      return Tip.api().get()
    },
    tipsGroupedByTask (tips) {
      return groupBy(tips, (tip) => {
        return tip.task ? tip.task.name : ''
      })
    },
    setProjectFilter (val) {
      this.projectFilter = val
      const tipsOfProject = Tip.query().where('projectId', val).get()
      const notContainingTask = tipsOfProject.filter(t => t.taskId === this.taskFilter).length === 0
      if (notContainingTask) {
        this.taskFilter = null
      }
      this.updateFilters()
    },
    setTaskFilter (val) {
      const tipsOfTask = Tip.query().where('taskId', val).get()
      // tipsOfTask can't be empty because it only uses taskId with at least a tip.
      this.projectFilter = tipsOfTask[0].projectId
      this.taskFilter = val
      this.updateFilters()
    },
    setCreatorFilter (val) {
      this.creatorFilter = val
      this.updateFilters()
    },
    updateFilters () {
      return this.$router.push({ name: 'tip-list', query: this.tipParams })
    }
  }
}
</script>

<template>
  <div class="tip-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="tip-list__container flex-grow-1">
      <app-header reduced />
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
            :project-id="query[FILTER_TYPES.PROJECT]"
            @update:projectId="setProjectFilter"
            :task-id="query[FILTER_TYPES.TASK]"
            @update:taskId="setTaskFilter"
            :creator-id="query[FILTER_TYPES.CREATOR]"
            @update:creatorId="setCreatorFilter"/>
            <div v-for="(projectValue, name) in tipsGroupedByProject" :key="name" class="mt-4 mb-4 border-bottom">
              <h1 class="mb-3 mt-4 primary">{{ name }}</h1>
              <div v-for="(taskValue, taskName) in tipsGroupedByTask(projectValue)" :key="taskName" class="mb-4">
                <h2 class="mb-4 ml-4 mt-4">{{ taskName }}</h2>
                <b-list-group-item v-for="tip in taskValue" class="flex-column align-items-start ml-4 border-0" :key="tip.id">
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
   h1 {
     color: $primary;
   }

   h2 {
     color: $tertiary;
   }
 }
</style>
