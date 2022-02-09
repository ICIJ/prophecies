<script>
import PageHeader from '@/components/PageHeader'
import UserNotifications from '@/components/UserNotifications'
import User from '@/models/User'

export default {
  name: 'UserRetrieveBookmarks',
  components: {
    PageHeader,
    UserNotifications
  },
  props: {
    username: {
      type: String
    }
  },
  computed: {
    user () {
      return User.find(this.username)
    }
  }
}
</script>

<template>
  <div class="user-retrieve-notifications">
    <user-notifications />
  </div>
</template>
