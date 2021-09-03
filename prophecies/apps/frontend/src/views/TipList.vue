<script>
import { get, groupBy, split, uniqueId } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import TipCard from '@/components/TipCard'
import Tip from '@/models/Tip'

export default {
  name: 'Tips',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter,
    TipCard
  },
  created() {
    return this.setup()
  },
  computed: {
    fetchTipsLoader () {
      return uniqueId('load-tips-')
    },
    tips () {
      return Tip.query().with('project').with('creator').with('task').with('task.project').all()
    },
    tipsGroupedByProject () {
      return groupBy(this.tips, (tip) => {
        return tip.project.name
      })
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
        return tip.task.name
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
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchTipsLoader" waiter-class="my-5 mx-auto d-block">
          <div v-if="tips">
            <div v-for="(projectValue, name) in tipsGroupedByProject" class="mt-4 mb-4 border-bottom">
              <h1 class="mb-3 mt-4">{{ name }}</h1>
              <div v-for="(taskValue, name) in tipsGroupedByTask(projectValue)" class="mb-4">
                <h2 class="mb-4 ml-4 mt-4">{{ name }}</h2>
                <b-list-group-item v-for="tip in taskValue" class="flex-column align-items-start ml-4 border-0" >
                  <tip-card :tip="tip" />
                </b-list-group-item>
              </div>
            </div>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>