<script>
import settings from '@/settings'
import store from '@/store'

export default {
  name: 'UserRetrieveLanguage',
  components: {},
  filters: {},
  computed: {
    locale: {
      get() {
        return store.state.app.locale ?? 'en'
      },
      set(value) {
        store.dispatch('app/locale', value)
        this.$core.loadLocale(value)
      }
    },
    locales() {
      return settings.locales
    },
    loadedLocales() {
      return this.$core.loadedLocales
    }
  },
  methods: {
    selectLocale(event) {
      this.locale = event.currentTarget.id
    }
  }
}
</script>

<template>
  <div class="user-retrieve-language">
    <ul class="user-retrieve-language__list p-0">
      <li
        v-for="availableLocale in locales"
        :id="availableLocale.key"
        :key="availableLocale.key"
        class="user-retrieve-language__list__language list-unstyled py-2"
        :style="{ cursor: 'pointer' }"
        @click="selectLocale"
      >
        <span :class="{ invisible: locale !== availableLocale.key }">
          <check-icon size="1.4x" />
        </span>
        <span class="px-2" :class="{ 'font-weight-bold': locale === availableLocale.key }">
          {{ availableLocale.label }} ({{ availableLocale.key.toUpperCase() }})
        </span>
      </li>
    </ul>
  </div>
</template>
