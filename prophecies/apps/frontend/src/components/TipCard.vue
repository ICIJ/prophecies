<script>
import { formatDateFromNow, formatDateLong } from '@/utils/date'
import Tip from '@/models/Tip'
import UserLink from '@/components/UserLink'

export default {
  name: 'TipsCard',
  components: {
    UserLink
  },
  filters: {
    formatDateLong(d) {
      return formatDateLong(d)
    },
    formatDateFromNow(d) {
      return formatDateFromNow(d)
    }
  },
  props: {
    tipId: {
      type: String
    },
    contentClass: {
      type: Object,
      default: () => ({
        tipCardMargin: 'mb-4',
        tipNameMargin: 'mb-5',
        tipDescriptionPadding: 'py-0'
      })
    }
  },
  computed: {
    tip() {
      return Tip.query().with('creator').find(this.tipId)
    }
  }
}
</script>

<template>
  <div :class="contentClass['tipCardMargin']" class="tip-card">
    <slot name="tip-name">
      <h2 :class="contentClass['tipNameMargin']">
        {{ tip.name }}
      </h2>
    </slot>
    <div :class="contentClass['tipDescriptionPadding']" v-html="tip.descriptionHTML"></div>
    <div class="text-right text-secondary">
      {{ $t('tips.lastModified') }}:
      <strong>
        <user-link class="text-truncate" :user-id="tip.creator.id" no-card>
          {{ tip.creator.displayName }}
          <template v-if="tip.creator.isMe">({{ $t('tips.you') }})</template>
        </user-link> </strong
      >,
      <router-link
        v-b-tooltip.hover
        :to="{ name: 'tip-retrieve', params: { tipId } }"
        :title="tip.updatedAt | formatDateLong"
        class="text-secondary"
      >
        {{ tip.updatedAt | formatDateFromNow }}
      </router-link>
    </div>
  </div>
</template>
