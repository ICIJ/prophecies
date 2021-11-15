<template>
  <div :class="contentClass['tipCardMargin']" class="tip-card">
    <slot name="tip-name"> 
      <h2 :class="contentClass['tipNameMargin']">
        {{ tip.name }}
      </h2>
    </slot>
    <div :class="contentClass['tipDescriptionPadding']" v-html="tip.descriptionHTML"></div>
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
    },
    contentClass: {
      type: Object,
      default: () => ({
          'tipCardMargin': 'mb-4',
          'tipNameMargin': 'mb-5',
          'tipDescriptionPadding': 'py-0'
      })
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
