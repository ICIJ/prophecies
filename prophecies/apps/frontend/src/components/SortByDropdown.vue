<template>
<div class="sort-by-dropdown d-flex align-items-start flex-column">
    <label :for="dropdownId" class="sort-by-dropdown__label text-primary mb-1">Sort by</label>
    <multiselect :allow-empty="false"
                  :show-labels="false"
                  :searchable="false"
                  :options="options"
                  :value="selectedSortOption"
                  placeholder="Sort by"
                  @input="intermediarySort = $event.value"
                  label="label"
                  track-by="value"
                  class="sort-by-dropdown__select "/>

</div>
</template>

<script>
import { find, uniqueId } from 'lodash'

import Multiselect from 'vue-multiselect'

export default {
  name: 'SortByDropdown',
  components: {
    Multiselect
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
      intermediarySort: this.sort,
      dropdownId: uniqueId('sortByDropdown-')
    }
  },
  computed: {
    selectedSortOption () {
      return find(this.options, { value: this.intermediarySort })
    }
  },
  watch: {
    intermediarySort (value) {
      this.$emit('update:sort', value)
    }
  }
}
</script>
<style lang='scss' scoped>
  .sort-by-dropdown{
    flex:0 1 270px;
    &__label{
    }
  }
</style>
