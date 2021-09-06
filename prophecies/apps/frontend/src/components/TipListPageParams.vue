<template>
  <div class="tip-list-page-params d-inline-flex">
    <div class="tip-list-page-params__project pr-3">
      <multiselect :allow-empty ="true"
                   :show-labels="false"
                   :searchable="false"
                   :options="projectOptions"
                   @input="$emit('applyProjectFilter', $event.value)"
                   label="label"
                   track-by="value" />
    </div>
    <div class="tip-list-page-params__task pr-3">
      <multiselect :allow-empty ="true"
                   :show-labels="false"
                   :searchable="false"
                   :options="taskOptions"
                   @input="$emit('applyTaskFilter', $event.value)"
                   label="label"
                   track-by="value" />
    </div>
    <div class="tip-list-page-params__creator pr-3">
      <multiselect :allow-empty ="true"
                   :show-labels="false"
                   :searchable="false"
                   :options="creatorOptions"
                   @input="$emit('applyCreatorFilter', $event.value)"
                   label="label"
                   track-by="value" />
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
      project: {
        type: String,
        default: ''
      },
      task: {
        type: String,
        default: ''
      },
      creator: {
        type: String,
        default: ''
      }
    },
    created() {
      return this.setup()
    },
    computed: {
      projectOptions () {
        const projects = Project.all()
        return map(projects, (project) => {
          return { value: project.id, label: project.name }
        })
      },
      taskOptions () {
        const tasks = Task.all()
        return map(tasks, (task) => {
          return { value: task.id, label: task.name }
        })
      },
      creatorOptions () {
        const users = User.all()
        return map(users, (user) => {
          return { value: user.id, label: user.username }
        })
      }
    },
    methods: {
      setup () {
        try {
          this.fetchTaskOptions()
          this.fetchProjectOptions()
          this.fetchCreatorOptions()
        } catch(error) {
          console.log(error);
        }
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

<style lang="scss" scoped>
</style>
