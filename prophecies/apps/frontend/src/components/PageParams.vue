<template>
  <div class="page-params">
    <div class="row">
      <label class="page-params__project col-lg-4 col-xl-3">
        <div class="mb-3">{{ $t('pageParams.project') }}</div>
        <multiselect
          :allow-empty="true"
          :show-labels="false"
          :options="projectOptions"
          :value="selectedProjectOption"
          :placeholder="$t('pageParams.selectAProject')"
          label="name"
          track-by="id"
          @input="$emit('update:projectId', idOrNull($event))"
        />
      </label>
      <label class="page-params__task col-lg-4 col-xl-3">
        <div class="mb-3">{{ $t('pageParams.task') }}</div>
        <multiselect
          :allow-empty="true"
          :show-labels="false"
          :options="taskOptions"
          :value="selectedTaskOption"
          :placeholder="$t('pageParams.selectATask')"
          label="name"
          track-by="id"
          @input="$emit('update:taskId', idOrNull($event))"
        >
          <template slot="option" slot-scope="{ option }">
            {{ option.name }}
            <span
              v-if="option.status !== 'OPEN'"
              class="page-params__task__show-status float-right text-capitalize font-weight-normal"
              >{{ option.status }}</span
            >
          </template>
        </multiselect>
      </label>
      <label v-if="creatorId !== undefined" class="page-params__creator col-lg-4 col-xl-3">
        <div class="mb-3">{{ $t('pageParams.author') }}</div>
        <multiselect
          :allow-empty="true"
          :show-labels="false"
          :options="creatorOptions"
          :value="selectedCreatorOption"
          :placeholder="$t('pageParams.selectAnAuthor')"
          label="displayName"
          track-by="id"
          @input="$emit('update:creatorId', idOrNull($event))"
        />
      </label>
    </div>
  </div>
</template>

<script>
import { find } from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'PageParams',
  components: {
    Multiselect
  },
  props: {
    values: {
      type: Array,
      default: () => []
    },
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
      default: undefined
    }
  },
  computed: {
    projectOptions() {
      return this.retrieveUniqueAssociatedEntity('project', 'projectId', 'name')
    },
    taskOptions() {
      return this.retrieveUniqueAssociatedEntity('task', 'taskId', 'name')
    },
    creatorOptions() {
      return this.retrieveUniqueAssociatedEntity('creator', 'creatorId', 'displayName')
    },
    selectedProjectOption() {
      return find(this.projectOptions, { id: this.projectId })
    },
    selectedTaskOption() {
      return find(this.taskOptions, { id: this.taskId })
    },
    selectedCreatorOption() {
      return find(this.creatorOptions, { id: this.creatorId })
    }
  },
  methods: {
    idOrNull(obj = null) {
      return obj && 'id' in obj ? obj.id : null
    },
    retrieveUniqueAssociatedEntity(elType, elId, elValue) {
      const elements = this.values.reduce((options, currentObject) => {
        const elementId = currentObject[elId] ?? currentObject.id
        const elementType = currentObject[elType] === undefined ? currentObject : currentObject[elType]
        if (elementType) {
          const elementName = elementType[elValue]
          if (elementId && !options[elementId]) {
            options[elementId] = {
              id: elementId,
              [elValue]: elementName
            }
            if (elType === 'task' && elementType.status) {
              options[elementId].status = elementType.status?.toLowerCase()
            }
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
.page-params {
  &__task {
    &__show-status {
      font-size: smaller;
    }
  }
}
</style>
