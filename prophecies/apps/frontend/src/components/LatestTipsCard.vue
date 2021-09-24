<template>
  <div class="latest-tips-card card card-body py-4 px-5 shadow">
    <div class="d-flex align-items-center mt-3 mb-5">
      <smile-icon class="text-primary mr-4" />
      <h1 class="latest-tips-card__title text-primary mb-0 font-weight-bold">
        Latest tips
      </h1>
    </div>
    <ul class="list-unstyled latest-tips-card__tips" v-if="latestTips && latestTips.length">
      <li class="latest-tips-card__tips__item" v-for="tip in latestTips">
        <div class="row">
          <div class="col">
            <a :href="tipLink(tip)">
              <h2 class="latest-tips-card__tips__item__title font-weight-bold">
                {{ tip.name }}
              </h2>
            </a>
            <div class="negative-margin text-black-50">
              <small v-if="tip.task">
                in {{ tip.task.name }} | {{ tip.project.name }}
              </small>
              <small v-else>
                General
              </small>
            </div>
          </div>
          <div class="col" v-html="tip.descriptionHTML"></div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { slice } from 'lodash'

export default {
  name: 'LatestTipsCard',
  props: {
    tips: {
      type: Array
    }
  },
  computed: {
    latestTips () {
      if (this.tips.length) {
        return this.tips.length > 3 ? slice(this.tips, 0, 2) : this.tips
      }
    }
  },
  methods: {
    tipLink (tip) {
      return `#/tips/${tip.id}`
    }
  }
}

</script>

<style lang="scss" scoped>
  .latest-tips-card {

    &__title {
      position: relative;
      padding-bottom: $spacer;

      &:after {
        content: "";
        width: 180%;
        max-width: 210px;
        position: absolute;
        bottom: 0%;
        left: 0;
        height: 7px;
        background: $warning;
        font-weight: 600;
      }
    }

    &__tips {

      &__item {
        margin-bottom: $spacer-lg;

        &__title {
          font-weight: 600;
          margin-bottom: $spacer-lg;
        }

        .negative-margin {
          margin-top: -15px
        }
      }
    }
  }
</style>
