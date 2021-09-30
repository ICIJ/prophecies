<template>
  <div class="shortcut-list d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="shortcut-list__container flex-grow-1">
      <app-header reduced />
      <div class="container-fluid pl-4 pt-5">
        <app-waiter :loader="fetchChoiceGroupsLoader" waiter-class="my-5 mx-auto d-block">
          <div class="shortcut-list__card p-5 w-75">
            <div class="row px-3 py-4" v-for="shortCut in defaultShortcuts">
              <div class="col font-weight-bold">
                {{ shortCut.name }}
              </div>
              <div class="col-10 text-primary font-weight-bold text-capitalize">
                {{ shortCut.value }}
              </div>
            </div>
            <div class="row px-3 py-4" v-for="shortCut in choiceGroups">
              <div class="col font-weight-bold">
                name tbd
              </div>
              <div class="col-10 text-primary font-weight-bold text-capitalize">
                {{ shortCut.shortkeys }}
              </div>
            </div>
          </div>
        </app-waiter>
      </div>
    </div>
  </div>

</template>

<script>
import { uniqueId, flatMap } from 'lodash'
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import AppWaiter from '@/components/AppWaiter'
import ChoiceGroup from '@/models/ChoiceGroup'

export default {
  name: 'ShortcutList',
  components: {
    AppSidebar,
    AppHeader,
    AppWaiter
  },
  data () {
    return {
      defaultShortcuts: [
        {
          name: 'Search',
          value: 'Ctrl + F'
        },
        {
          name: 'Leave a note',
          value: 'N'
        }
      ]
    }
  },
  computed: {
    fetchChoiceGroupsLoader () {
      return uniqueId('load-choice-groups-')
    },
    choiceGroups () {
      const choiceGroups = ChoiceGroup.query().with('choices').get()
      return flatMap(choiceGroups, 'choices')
    }
  },
  created() {
    return this.setup()
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchChoiceGroupsLoader, this.fetchChoiceGroups)
      } catch (error) {
        const title = 'Unable to retrieve shortcuts'
        this.$router.replace({ name: 'error', params: { title, error } })
      }
    },
    async waitFor (loader, fn) {
      this.$wait.start(loader)
      await fn()
      this.$wait.end(loader)
    },
    fetchChoiceGroups () {
      return ChoiceGroup.api().get()
    }
  }

}
</script>

<style lang="scss" scoped>
  .shortcut-list {
    &__card {
      background-color: rgba($primary, .1);
      border-radius: $card-border-radius;
    }
  }
</style>
