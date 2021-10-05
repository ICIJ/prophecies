<template>
  <div class="shortcut-list-card">
    <app-waiter :loader="fetchChoiceGroupsLoader" waiter-class="my-5 mx-auto d-block">
      <div :class="width" class="shortcut-list-card__card p-5">
        <div class="row px-3 py-4" v-for="shortCut in defaultShortcuts">
          <div class="col font-weight-bold">
            {{ shortCut.name }}
          </div>
          <div class="col-10 col-sm-8 text-primary font-weight-bold text-capitalize">
            {{ shortCut.value }}
          </div>
        </div>
        <div class="row px-3 py-4" v-for="shortCut in choiceGroups">
          <div class="col font-weight-bold">
            {{ generateName(shortCut.value) }}
          </div>
          <div class="col-sm-8 text-primary font-weight-bold text-capitalize">
            {{ shortCut.shortkeys }}
          </div>
        </div>
      </div>
    </app-waiter>
  </div>
</template>

<script>
import { uniqueId, flatMap } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import ChoiceGroup from '@/models/ChoiceGroup'
import ShortcutListCard from '@/components/ShortcutListCard'

export default {
  name: 'ShortcutList',
  components: {
    AppWaiter
  },
  props: {
    width: {
      type: String,
      default: 'w-100'
    },
    showClose: {
      type: Boolean,
      default: false
    }
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
    },
    generateName (value) {
      return `Mark as ${value}`
    }
  }
}
</script>

<style lang="scss" scoped>
  .shortcut-list-card {
    &__card {
      background-color: rgba($primary, .1);
      border-radius: $card-border-radius;
    }
  }
</style>
