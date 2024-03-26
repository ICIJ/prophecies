<script>
export default {
  name: 'AppVersion',
  computed: {
    version() {
      return this.$config.get('version', '0.0.0')
    }
  }
}
</script>

<template>
  <span class="app-version">
    {{ $t('appVersion.version', { version }) }}
  </span>
</template>
