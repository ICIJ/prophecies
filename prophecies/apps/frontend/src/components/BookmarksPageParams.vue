<template>
  <div class="bookmarks-page-params">
    <div class="row">
      <label class="bookmarks-page-params__project col-lg-4 col-xl-3">
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
      <label class="bookmarks-page-params__task col-lg-4 col-xl-3">
        <div class="mb-3">Task</div>
        <multiselect :allow-empty ="true"
                     :show-labels="false"
                     :options="taskOptions"
                     :value="selectedTaskOption"
                     @input="$emit('update:taskId', idOrNull($event))"
                     placeholder="Select a task"
                     label="name"
                     track-by="id">
          <template slot="option" slot-scope="{ option }">
            {{ option.name }} <span v-if="option.status !== 'OPEN'" class='bookmarks-page-params__task__show-status float-right text-capitalize font-weight-normal'>{{ option.status}}</span>
          </template>
        </multiselect>
      </label>
    </div>
  </div>
</template>

<script>
import { find } from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'BookmarksPageParams',
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
    tasks: {
      type: Array
    }
  },
  created () {
    return this.setup()
  },
  computed: {
    projectOptions () {
      return this.retrieveUniqueAssociatedEntity(this.tasks.map(task => task.project),'project')
    },
    taskOptions () {
      return this.retrieveUniqueAssociatedEntity(this.tasks, 'task')
    },
    selectedProjectOption () {
      return find(this.projectOptions, { id: this.projectId })
    },
    selectedTaskOption () {
      return find(this.taskOptions, { id: this.taskId })
    }
  },
  methods: {
    setup () {

    },
    idOrNull (obj = null) {
      return obj && 'id' in obj ? obj.id : null
    },
    retrieveUniqueAssociatedEntity (collection, elType) {
      const elements = collection.reduce((options, element) => {
        const elementId = element['id']
        const elementName = element['name']
        if (elementId && !options[elementId]) {
          options[elementId] = {
            id: elementId,
            ['name']: elementName
          }
          if (elType === 'task') {
            const status = element.status
            options[elementId].status = status.toLowerCase()
          }
        }
        return options
      }, {})
      return Object.values(elements)
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
