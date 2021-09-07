<template>
  <div class="tip-list-page-params container-fluid">
    <div class="row">
      <label class="tip-list-page-params__project col-lg-4 col-xl-3">
        <div class="mb-3">Project</div>
        <multiselect :allow-empty ="true"
                     :show-labels="false"
                     :options="projectOptions"
                     :value="selectedProjectOption"
                     @input="$emit('update:projectId', idOrNull($event))"
                     placeholder="Select a project"
                     label="name"
                     track-by="id" />
      </label>
      <label class="tip-list-page-params__task col-lg-4 col-xl-3">
        <div class="mb-3">Task</div>
        <multiselect :allow-empty ="true"
                     :show-labels="false"
                     :options="taskOptions"
                     :value="selectedTaskOption"
                     @input="$emit('update:taskId', idOrNull($event))"
                     placeholder="Select a task"
                     label="name"
                     track-by="id" />
      </label>
      <label class="tip-list-page-params__creator col-lg-4 col-xl-3">
        <div class="mb-3">Author</div>
        <multiselect :allow-empty ="true"
                     :show-labels="false"
                     :options="creatorOptions"
                     :value="selectedCreatorOption"
                     @input="$emit('update:creatorId', idOrNull($event))"
                     placeholder="Select an author"
                     label="displayName"
                     track-by="id" />
      </label>
    </div>
  </div>
</template>

<script>
  import { find, map } from 'lodash'
  import Multiselect from 'vue-multiselect'

  import Project from '@/models/Project'
  import Task from '@/models/Task'
  import User from '@/models/User'

  export default {
    name: 'TipListPageParams',
    components: {
      Multiselect
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
    created() {
      return this.setup()
    },
    computed: {
      projectOptions () {
        return Project.all()
      },
      taskOptions () {
        return Task.all()
      },
      creatorOptions () {
        return User.all()
      },
      selectedProjectOption () {
        return find(this.projectOptions, { id: this.projectId })
      },
      selectedTaskOption () {
        return find(this.taskOptions, { id: this.taskId })
      },
      selectedCreatorOption () {
        return find(this.creatorOptions, { id: this.creatorId })
      }
    },
    methods: {
      setup () {
        this.fetchTaskOptions()
        this.fetchProjectOptions()
        this.fetchCreatorOptions()
      },
      idOrNull (obj = null) {
        return obj && 'id' in obj ? obj.id : null
      },
      fetchProjectOptions () {
        return Project.api().get()
      },
      fetchTaskOptions () {
        return Task.api().get()
      },
      fetchCreatorOptions () {
        return User.api().get()
      }
    }
  }
</script>
