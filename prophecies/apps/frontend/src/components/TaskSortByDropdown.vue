<template>
    <sort-by-dropdown
      :sort.sync="sortField"
      :options="sortOptions"
      class="mb-3 task-sort-by-dropdown"
      >
      <template #label>
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
        { value: 'status_asc', label: this.$t('taskSortByDropdown.status'), $isDefault: true, needStatus: true },
        { value: 'progress_asc', label: this.$t('taskSortByDropdown.progress0_100') },
        { value: 'progress_desc', label: this.$t('taskSortByDropdown.progress100_0') },
        { value: 'priority_asc', label: this.$t('taskSortByDropdown.priority0_9'), needStatus: true },
        { value: 'priority_desc', label: this.$t('taskSortByDropdown.priority9_0'), needStatus: true },
        { value: 'name_asc', label: this.$t('taskSortByDropdown.nameAZ') },
        { value: 'name_desc', label: this.$t('taskSortByDropdown.nameZA') },
        { value: 'createdAt_desc', label: this.$t('taskSortByDropdown.recentlyCreated') }
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
        return TaskStatusOrder[task.status] === 1
      }
    },
    sortField: {
      get () {
        const isParamValid = find(this.sortOptions, { value: this.$route.query.sort })
        return isParamValid ? this.$route.query.sort : this.sort
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
        if (this.selectedSortName === 'status') {
          return orderBy(tasks, [this.sortByStatus, 'name'], ['asc', 'asc'])
        } else if (this.selectedSortOption.needStatus) { // adding this condition can help ignoring the closed tasks on priority sorting
          return orderBy(tasks, [this.sortByStatus, this.selectedSortName, 'name'], ['asc', this.selectedSortOptionOrder, 'asc', 'asc'])
        } else {
          return orderBy(tasks, [this.selectedSortName, 'name'], [this.selectedSortOptionOrder, 'asc'])
        }
      }
    }

  }
}
</script>
