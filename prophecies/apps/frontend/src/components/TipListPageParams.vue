<template>
  <page-params
    :values='tips'
    :projectId.sync="projectId_"
    :taskId.sync="taskId_"
    :creatorId.sync="creatorId_"
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
    },
    projectId_: {
      get () {
        return this.projectId
      },
      set (value) {
        this.$emit('update:projectId', value)
      }
    },
    taskId_: {
      get () {
        return this.taskId
      },
      set (value) {
        this.$emit('update:taskId', value)
      }
    },
    creatorId_: {
      get () {
        return this.creatorId
      },
      set (value) {
        this.$emit('update:creatorId', value)
      }
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
