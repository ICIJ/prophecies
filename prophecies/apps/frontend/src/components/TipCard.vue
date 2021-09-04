<template>
  <div class="tip-card">
    <div class="d-flex w-100 justify-content-between mt-3">
      <h2>
        {{ tip.name }}
      </h2>
    </div>
    <div class="my-3" v-html="tip.descriptionHTML"></div>
    <div class="text-right text-secondary">
      Last modified: <strong>{{ tip.creator.username }}</strong>,
      <router-link
        :to="{ name: 'tip-retreive', params: { tipId } }"
        :title="tip.updatedAt | formatDateLong"
        v-b-tooltip.hover
        class="text-secondary">
        {{ tip.updatedAt | formatDateFromNow }}
      </router-link>
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
  computed: {
    tipId () {
      return this.tip.id
    }
  },
  filters: {
    formatDateLong (d) {
      return moment(d).format('MMM Do YYYY - hh:mm')
    },
    formatDateFromNow (d) {
      return moment(d).fromNow()
    }
  },
}
</script>
