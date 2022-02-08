<script>
import { formatDateLongAlt } from '@/utils/date'
import User from '@/models/User'
import UserCard from '@/components/UserCard.vue'

export default {
  name: 'UserRetrieveProfile',
  components: {
    UserCard
  },
  props: {
    username: {
      type: String
    }
  },
  filters: {
    formatDate (d) {
      return formatDateLongAlt(d)
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
  <user-card :username="username" class="user-retrieve-profile">
    <template #content :user={user}>
      <ul class="list-unstyled mt-5" >
        <li class="user-retrieve-profile__super-user mb-3" v-if="user.isSuperuser">
          <span class="d-inline-flex py-0 px-3 bg-warning rounded align-items-center text-primary">
            <award-icon size="1.5x" class="my-2 mr-2" />
            Admin
          </span>
        </li>
        <li class="user-retrieve-profile__email mb-3">
          Email: <a v-if="user.email" :href="`mailto:${user.email}`">{{ user.email }}</a><template v-else>{{$t('userRetrieveProfile.notProvided')}}</template>
        </li>
        <li class="user-retrieve-profile__last-login">
          {{$t('userRetrieveProfile.lastLogin')}}: {{ user.lastLogin | formatDate }}
        </li>
      </ul>
    </template>
  </user-card>
</template>
