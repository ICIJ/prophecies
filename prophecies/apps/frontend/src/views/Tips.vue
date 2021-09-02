<template>
  <div class="tips d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="tips__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchTipsLoader" waiter-class="my-5 mx-auto d-block">
          <div v-if="tips">
            <b-list-group v-for="(projectValue, name) in tipsGroupedByProject" class="mt-4 mb-4 border-bottom">
              <h1 class="mb-3 mt-4">{{ name }}</h1>
              <b-list-group v-for="(taskValue, name) in tipsGroupedByTask(projectValue)" class="mb-4">
                <h2 class="mb-4 ml-4 mt-4">{{ name }}</h2>
                <b-list-group-item v-for="tip in taskValue" class="flex-column align-items-start ml-4 border-0" >
                  <div class="d-flex w-100 justify-content-between mt-3">
                    <h2> {{tip.name}} </h2>
                  </div>
                  <p class="mb-1 mt-3">
                    {{ tip.description }}
                  </p>
                  <div class="mt-3">
                    <b-row align-h="end">
                      <b-col cols="auto" class="p-3">Last modified: {{ tip.creator.username }}, {{ formatDate(tip.updatedAt) }}</b-col>
                      <b-col cols="auto" class="p-3"> <a href="#">Edit</a> </b-col>
                    </b-row>
                  </div>
                </b-list-group-item>
              </b-list-group>
            </b-list-group>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>
</template>

<script>
import { get, groupBy, uniqueId, split } from 'lodash'
import moment from 'moment'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import Tip from '@/models/Tip'

export default {
  name: 'Tips',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter
  },
  props: {

  },
  data () {
    return {
    }
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
    },
    formatDate (date) {
      return moment(date).format('MMM Do YYYY - hh:mm')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
