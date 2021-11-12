<template>
    <sort-by-dropdown
      :sort.sync="sortField"
      :options="sortOptions"
      class="mb-3 task-sort-by-dropdown"
      >
      <template #label>
            <div class="mb-1 text-primary">Sort by</div>
      </template>
    </sort-by-dropdown>
</template>

<script>
import { find, orderBy } from 'lodash'
import SortByDropdown from '@/components/SortByDropdown.vue'
import { TaskStatusOrder } from '@/models/Task'

export default {
  name: 'TaskSortByDropdown',
  components: {
    SortByDropdown
  },
  model: {
    prop: 'sort',
    event: 'update:sort'
  },
  props: {
    sort: {
      type: String,
      default: null
    },
    options: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      sortOptions: [
        { value: 'name_asc', label: 'Name (A-Z)', $isDefault: true },
        { value: 'name_desc', label: 'Name (Z-A)' },
        // { value: 'lastReviewed_desc', label: 'Recently reviewed' },
        { value: 'createdAt_desc', label: 'Recently created' },
        { value: 'priority_asc', label: 'Priority (0-9)' },
        { value: 'priority_desc', label: 'Priority (9-0)' },
        { value: 'progress_asc', label: 'Progress (0%-100%)' },
        { value: 'progress_desc', label: 'Progress (100%-0%)' }
      ]
    }
  },
  computed: {
    selectedSortOption () {
      return find(this.sortOptions, { value: this.sortField })
    },
    selectedSortName () {
      return this.selectedSortOption.value.split('_')[0]
    },
    selectedSortOptionOrder () {
      return this.selectedSortOption.value.split('_')[1]
    },
    sortByStatus () {
      return function (task) {
        return TaskStatusOrder[task.status] === 0
      }
    },
    sortField: {
      get () {
        const isParamValid = find(this.sortOptions, { value: this.$route.query.sort })
        if (!isParamValid) {
          return this.sort
        } else {
          return this.$route.query.sort
        }
      },
      set (value) {
        const query = { ...this.$route.query, sort: value }
        this.$router.push({ path: this.$route.path, query }, null)
        this.$emit('update:sort', value)
        this.$emit('update:sort-by-cb', this.callbackOrderBy.bind(this))
      }
    },
    callbackOrderBy () {
      return (tasks) => {
        return orderBy(tasks, [this.selectedSortName, this.sortByStatus, 'name'], [this.selectedSortOptionOrder, 'asc', 'asc'])
      }
    }

  }
}
</script>
