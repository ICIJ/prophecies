<template>
  <page-params
    :values='tips'
    :projectId="projectId"
    @update:projectId="$emit('update:projectId',$event)"
    :taskId="taskId"
    @update:taskId="$emit('update:taskId',$event)"
    :creatorId="creatorId"
    @update:creatorId="$emit('update:creatorId',$event)"
    class="tip-list-page-params"
  />
</template>

<script>
import Tip from '@/models/Tip'
import PageParams from '@/components/PageParams'

export default {
  name: 'TipListPageParams',
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
    creatorId: {
      type: String,
      default: ''
    }
  },
  created () {
    return this.fetchTips()
  },
  computed: {
    tips () {
      return Tip.query()
        .with('project')
        .with('task')
        .with('creator')
        .get()
    }

  },
  methods: {
    fetchTips () {
      return Tip.api().get()
    }
  }
}
</script>

<style lang="scss">
  .tip-list-page-params {
    &__task {
      &__show-status {
        font-size: smaller;
      }
    }
  }
</style>
