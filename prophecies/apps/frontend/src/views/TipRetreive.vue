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
  props: {
    tipId: {
      type: [String, Number]
    }
  },
  created() {
    return this.setup()
  },
  computed: {
    fetchTipLoader () {
      return uniqueId('load-tip-')
    },
    tip () {
      return Tip
        .query()
        .with('project')
        .with('creator')
        .with('task')
        .with('task.project')
        .find(this.tipId)
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
        await this.waitFor(this.fetchTipLoader, this.fetchTip)
      } catch (error) {
        const title = 'Unable to retrieve the tip'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    fetchTip () {
      return Tip.api().get(this.tipId)
    }
  }
}
</script>

<template>
  <div class="tip-retreive d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="tip-retreive__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid p-5">
        <app-waiter :loader="fetchTipLoader" waiter-class="my-5 mx-auto d-block">
          <tip-card :tip="tip" />
        </app-waiter>
      </div>
    </div>
  </div>
</template>
