<script>
import { get, groupBy, uniqueId } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import LatestTipsCard from '@/components/LatestTipsCard'
import Tip from '@/models/Tip'
import TipCard from '@/components/TipCard'
import TipListPageParams from '@/components/TipListPageParams'

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
  data () {
    return {
      showLatestTips: true,
      projectFilter: null,
      taskFilter: null,
      creatorFilter: null,
      tipIds: []
    }
  },
  watch: {
    projectFilter () {
      return this.waitFor(this.fetchTipsLoader, this.fetchTips)
    },
    taskFilter () {
      return this.waitFor(this.fetchTipsLoader, this.fetchTips)
    },
    creatorFilter () {
      return this.waitFor(this.fetchTipsLoader, this.fetchTips)
    }
  },
  created () {
    return this.setup()
  },
  computed: {
    fetchTipsLoader () {
      return uniqueId('load-tips-')
    },
    tips () {
      return Tip.query()
        .with('project')
        .with('task')
        .whereIdIn(this.tipIds)
        .get()
    },
    tipsGroupedByProject () {
      return groupBy(this.tips, (tip) => {
        return tip.project ? tip.project.name : 'General'
      })
    },
    tipParams () {
      return {
        'filter[project]': this.projectFilter,
        'filter[task]': this.taskFilter,
        'filter[creator]': this.creatorFilter
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
    async fetchTips () {
      const params = this.tipParams
      const { response } = await Tip.api().get('', { params })
      const tipIds = get(response, 'data.data', []).map(t => t.id)
      this.$set(this, 'tipIds', tipIds)
    },
    tipsGroupedByTask (tips) {
      return groupBy(tips, (tip) => {
        return tip.task ? tip.task.name : ''
      })
    }
  }
}
</script>

<template>
  <div class="tip-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="tip-list__container flex-grow-1">
      <app-header reduced />
      <b-collapse :visible="showLatestTips">
        <latest-tips-card :tips="tips" :show-close="true" @close="showLatestTips = false" class="mx-4 mb-5">
          <template v-slot:title>
            <h1 class="latest-tips-card__title text-primary mb-0 font-weight-bold">
              Latest tips
            </h1>
          </template>
        </latest-tips-card>
      </b-collapse>
      <tip-list-page-params
        :project-id.sync="projectFilter"
        :task-id.sync="taskFilter"
        :creator-id.sync="creatorFilter" />
      <div class="container-fluid pl-4 pt-5">
        <app-waiter :loader="fetchTipsLoader" waiter-class="my-5 mx-auto d-block">
          <div v-if="tips">
            <div v-for="(projectValue, name) in tipsGroupedByProject" class="mt-4 mb-4 border-bottom" :key="projectValue">
              <h1 class="mb-3 mt-4 primary">{{ name }}</h1>
              <div v-for="(taskValue, name) in tipsGroupedByTask(projectValue)" class="mb-4" :key="taskValue">
                <h2 class="mb-4 ml-4 mt-4">{{ name }}</h2>
                <b-list-group-item v-for="tip in taskValue" class="flex-column align-items-start ml-4 border-0" :key="tip.id">
                  <tip-card :tip-id="tip.id" />
                </b-list-group-item>
              </div>
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
