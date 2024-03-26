<script>
import { get } from 'lodash'

import AppVersion from '@/components/AppVersion'
import User from '@/models/User'

export default {
  name: 'Error',
  components: {
    AppVersion
  },
  props: {
    error: {
      type: [String, Error],
      default: null
    },
    title: {
      type: String,
      default: null
    },
    description: {
      type: String,
      default: null
    },
    code: {
      type: Number,
      default: null
    }
  },
  computed: {
    codeAsString() {
      return this.code || get(this, 'error.response.status')
    },
    username() {
      const { username = null } = User.me() || {}
      return username
    },
    titleAsString() {
      if (!this.title) {
        return get(this, 'error.response.statusText', this.error)
      }
      return this.title
    },
    descriptionAsString() {
      if (!this.description) {
        return get(this, 'error.message')
      }
      return this.description
    },
    helpLink() {
      return this.$config.get('helpLink')
    },
    logoutLink() {
      return this.$config.get('logoutUrl')
    },
    showHeader() {
      return !!this.username
    }
  }
}
</script>

<template>
  <div class="error d-flex flex-column">
    <div v-if="showHeader" class="error__header p-3 text-right">
      <a
        v-b-tooltip.html
        class="btn btn-outline-light btn-sm"
        :href="logoutLink"
        :title="$t('error.connectedAs', { username })"
      >
        {{ $t('error.logout') }}
      </a>
    </div>
    <div class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="error__container container">
        <h1 class="mb-3 error__container__heading">
          <span class="error__container__heading__code mr-3">
            <frown-icon class="error__container__heading__code__icon" />
            <span class="px-2 error__container__heading__code__value">{{ codeAsString }}</span>
          </span>
          {{ titleAsString || $t('error.title') }}
        </h1>
        <p class="error__container__description lead">
          {{ descriptionAsString || $t('error.description') }}
        </p>
        <ul class="error__container__links list-inline text-capitalize">
          <li class="list-inline-item error__container__links__item">
            <app-version />
          </li>
          <li class="list-inline-item error__container__links__item">
            <a :href="helpLink" target="_blank">
              <life-buoy-icon />
              {{ $t('error.help') }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.error {
  background: $primary no-repeat right bottom;
  color: text-contrast($primary);
  width: 100%;
  min-height: 100vh;

  &__container {
    margin: $spacer auto;
    text-align: center;

    &__heading {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;

      &__code {
        display: inline-flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        background: $danger;
        border-radius: 1em;

        &__icon {
          transform: scale(1.1);
        }

        &__value {
          font-size: 0.8rem;

          &:empty {
            display: none;
          }
        }
      }
    }

    &__description {
      margin-bottom: $spacer * 5;
    }

    &__links {
      &__item {
        &:not(:last-of-type):after {
          content: '|';
          margin: 0 $spacer;
          color: $light;
        }

        &,
        a {
          color: $light;
        }
      }
    }
  }
}
</style>
