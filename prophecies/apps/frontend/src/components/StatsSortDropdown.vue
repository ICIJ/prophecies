<template>
<div class="stats-sort-dropdown">
    <!--<label>
        Sort by
      </label>
      <multiselect :allow-empty="false"
                   :show-labels="false"
                   :searchable="false"
                   :options="sortOptions"
                   :value="selectedSortOption"
                   @input="intermediarySort = $event.value"
                   label="label"
                   track-by="value" />-->
</div>
</template>

<script>

import Multiselect from 'vue-multiselect'

export default {
    name: 'StatsSortDropdown',
    components: {
        Multiselect
    },
    props: {

    }
}
</script>
