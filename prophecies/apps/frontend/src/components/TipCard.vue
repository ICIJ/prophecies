<template>
  <div class="tip-card">
    <div class="d-flex w-100 justify-content-between mt-3">
      <h2> {{tip.name}} </h2>
    </div>
    <p class="mb-1 mt-3">
      {{ tip.description }}
    </p>
    <div class="mt-3">
      <b-row align-h="end">
        <b-col cols="auto" class="p-3">Last modified: {{ tip.creator.username }}, {{ tip.updatedAt | formatDate }}</b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'TipsCard',
  props: {
    tip: {
      type: Object
    }
  },
  filters: {
    formatDate (d) {
      return moment(d).format('MMM Do YYYY - hh:mm')
    }
  }
}
</script>
