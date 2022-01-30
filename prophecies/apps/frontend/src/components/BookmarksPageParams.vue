<template>
  <page-params
    :values='tasks'
    :projectId="projectId"
    @update:projectId="$emit('update:projectId',$event)"
    :taskId="taskId"
    @update:taskId="$emit('update:taskId',$event)"
    class="bookmarks-page-params"
  />

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
      default: () => ([])
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
