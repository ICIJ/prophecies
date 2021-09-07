<template>
  <div class="tip-card">
    <h2 class="mb-5">
      {{ tip.name }}
    </h2>
    <div class="my-3" v-html="tip.descriptionHTML"></div>
    <div class="text-right text-secondary">
      Last modified: <strong>{{ tip.creator.displayName }}</strong>,
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
import Tip from '@/models/Tip'

export default {
  name: 'TipsCard',
  props: {
    tipId: {
      type: String
    }
  },
  computed: {
    tip () {
      return Tip
        .query()
        .with('creator')
        .find(this.tipId)
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
