<template>
  <div class="shortcut-list-card p-3">
    <app-waiter :loader="fetchTasksLoader" waiter-class="my-5 mx-auto d-block">
      <slot name="header" />
      <div :class="contentClass" class="shortcut-list-card__content px-5 pt-5 pb-0">
        <div class="row shortcut-list-card__content__row" v-for="(shortCut, i) in defaultShortcuts" :key="`general-shortcut-${i}`">
          <div class="col shortcut-list-card__content__row__name font-weight-bold">
            {{ shortCut.name }}
          </div>
          <div class="col text-primary font-weight-bold text-capitalize">
            {{ shortCut.value }}
          </div>
        </div>
        <div v-for="task in tasks" :key="task.id">
          <h3 class="text-primary mb-3">{{ task.name }}</h3>
          <div class="row shortcut-list-card__content__row" v-for="choice in task.choiceGroup.choices" :key="`task-${task.id}-shortcut-${choice.id}`">
            <div class="col shortcut-list-card__content__row__name font-weight-bold">
              {{ generateName(choice.value) }}
            </div>
            <div class="col text-primary font-weight-bold text-capitalize">
              {{ choice.shortkeys }}
            </div>
          </div>
        </div>
      </div>
      <slot name="footer" />
    </app-waiter>
  </div>
</template>

<script>
import { uniqueId, flatMap } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import Task from '@/models/Task'
import ShortcutListCard from '@/components/ShortcutListCard'

export default {
  name: 'ShortcutList',
  components: {
    AppWaiter
  },
  props: {
    contentClass: {
      type: [String, Object, Array],
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
    fetchTasksLoader () {
      return uniqueId('load-tasks-')
    },
    tasks () {
      return Task.query()
        .with('choiceGroup')
        .with('choiceGroup.choices')
        .get()
    }
  },
  created() {
    return this.setup()
  },
  methods: {
    async setup () {
      try {
        await this.waitFor(this.fetchTasksLoader, this.fetchTasks)
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
    fetchTasks () {
      const params = { include: 'choiceGroup.choices' }
      return Task.api().get('', { params })
    },
    generateName (value) {
      return `Mark as "${value}"`
    }
  }
}
</script>

<style lang="scss" scoped>
  .shortcut-list-card {
    background-color: $primary-10;
    border-radius: $card-border-radius;

    &__content {
      &__row {
        padding-bottom: $spacer-xl;   

        &__name {
          max-width: 200px;
          width: 100%;
        }
      }
    }
  }
</style>
