<template>
  <div class="tip-list-page-params">
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
                     track-by="id">
          <template slot="option" slot-scope="{ option }">
            <div class="d-flex">
              <div>
                {{ option.name }}
              </div>
              <div class="tip-list-page-params__task__show-status ml-auto text-capitalize font-weight-normal" v-if="option.status === 'closed'">
                {{ option.status }}
              </div>
            </div>
          </template>
        </multiselect>
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
import { find } from 'lodash'
import Multiselect from 'vue-multiselect'

import Tip from '@/models/Tip'

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
  created () {
    return this.setup()
  },
  computed: {
    tips () {
      return Tip.query()
        .with('project')
        .with('task')
        .with('creator')
        .get()
    },
    projectOptions () {
      return this.retrieveUniqueAssociatedEntity('project', 'projectId', 'name')
    },
    taskOptions () {
      return this.retrieveUniqueAssociatedEntity('task', 'taskId', 'name')
    },
    creatorOptions () {
      return this.retrieveUniqueAssociatedEntity('creator', 'creatorId', 'displayName')
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
      this.fetchTips()
    },
    idOrNull (obj = null) {
      return obj && 'id' in obj ? obj.id : null
    },
    fetchTips () {
      return Tip.api().get()
    },
    retrieveUniqueAssociatedEntity (elType, elId, elValue) {
      const elements = this.tips.reduce((options, tip) => {
        const elementId = tip[elId]
        const elementName = tip[elType]?.[elValue]
        if (elementId && !options[elementId]) { 
          options[elementId] = { 
            id: elementId, 
            [elValue]: elementName 
          }
          if (elType === 'task') {
            const status = tip[elType]?.status
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
  .tip-list-page-params {
    &__task {
      &__show-status {
        font-size: smaller;
      }
    }
  }
</style>
