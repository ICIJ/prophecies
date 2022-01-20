<script>
  import { template } from 'lodash'
  import User from '@/models/User'

  export default {
    name: 'UserAvatar',
    props: {
      userId: {
        type: [String, Number]
      },
      size: {
        type: [String, Number],
        default: 42
      }
    },
    computed: {
      user () {
        return User.find(this.userId)
      },
      userAvatarUrl () {
        const interpolate = this.$config.get('templateInterpolate')
        const avatarUrlTemplate = this.$config.get('avatarUrlTemplate')
        const compiled = template(avatarUrlTemplate, { interpolate })
        try {
          return compiled(this.user)
        } catch (_) {
          return null
        }
      }
    }
  }
</script>

<template>
  <img :src="userAvatarUrl" class="user-avatar rounded-circle" :height="size" :width="size" />
</template>