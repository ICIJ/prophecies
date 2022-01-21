<script>
  import User from '@/models/User'

  export default {
    name: 'UserLink',
    props: {
      userId: {
        type: [String, Number]
      },
      params: {
        type: Object,
        default: () => ({ })
      },
      useDisplayName: {
        type: Boolean
      }
    },
    computed: {
      user () {
        return User.find(this.userId)
      },
      to () {
        const username = this.user.username
        const params = { username, ...this.params }
        return { name: 'user-retreive-profile', params }
      },
      label () {
        if (this.useDisplayName) {
          return this.user.displayName
        }
        return `@${this.user.username}`
      }
    }
  }
</script>

<template>
  <router-link :to="to">
    <slot v-bind="{ user }">
      {{ label }}
    </slot>
  </router-link>
</template>