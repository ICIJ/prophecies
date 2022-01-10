<script>
export default {
  name: 'Login',
  computed: {
    loginUrl () {
      return this.$core.config.get('loginUrl')
    },
    loginWelcome () {
      return this.$core.config.get('loginWelcome') || this.$t('login.welcome')
    },
    loginAccountDescription () {
      return this.$core.config.get('loginAccountDescription') || this.$t('login.accountDescription')
    },
    loginAccountButton () {
      return this.$core.config.get('loginAccountButton') || this.$t('login.account')
    },
    helpDescription  () {
      return this.$core.config.get('helpDescription')
    },
    helpLink () {
      return this.$core.config.get('helpLink')
    }
  },
  async mounted () {
    if (await this.hasUser()) {
      return this.$router.push('/')
    }
  },
  methods: {
    async hasUser () {
      try {
        return !!await this.$core.getUser()
      } catch (_) {
        return false
      }
    }
  }
}
</script>

<template>
  <div class="login">
    <div class="login__card card text-center">
      <div class="login__card__heading card-title mt-4">
        <h2 class="display-4">{{ loginWelcome }}</h2>
        <p class="lead mb-0" v-html="$t('login.sumUp')"></p>
      </div>
      <div class="login__card__body">
        <ul class="list-group">
          <li class="list-group-item bg-muted border-top border-bottom border-left-0 border-right-0 rounded-0">
            <p>{{ loginAccountDescription }}</p>
            <a class="btn btn-dark btn-lg font-weight-bold" :href="loginUrl">
              <shield-icon size="1x" class="mr-1" />
              {{ loginAccountButton }}
            </a>
          </li>
          <li class="list-group-item border-0">
            <p>{{ helpDescription }}</p>
            <a class="btn btn-outline-tertiary btn-lg" :href="helpLink" target="_blank" :title="$t('login.askHelp')">
              <fa icon="ambulance" class="mr-2"></fa>
              {{ $t('login.askHelp') }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .login {
    background: theme-color('primary');
    min-height: 100vh;
    padding: 10vh;

    &__card {
      margin:0 auto;
      max-width: 660px;

      &__heading h2 {
        font-size: 2.5rem;
      }

      p:empty {
        display: none;
      }
    }
  }
</style>
