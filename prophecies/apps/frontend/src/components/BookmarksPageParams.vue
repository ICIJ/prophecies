<template>
  <page-params :values="tasks" :project-id.sync="projectId_" :task-id.sync="taskId_" class="bookmarks-page-params" />
</template>

<script>
import PageParams from '@/components/PageParams'

export default {
  name: 'BookmarksPageParams',
  components: {
    PageParams
  },
  props: {
    projectId: {
      type: String,
      default: ''
    },
    taskId: {
      type: String,
      default: ''
    },
    tasks: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    projectId_: {
      get() {
        return this.projectId
      },
      set(value) {
        this.$emit('update:projectId', value)
      }
    },
    taskId_: {
      get() {
        return this.taskId
      },
      set(value) {
        this.$emit('update:taskId', value)
      }
    }
  }
}
</script>

<style lang="scss">
.bookmarks-page-params {
  &__task {
    &__show-status {
      font-size: smaller;
    }
  }
}
</style>
