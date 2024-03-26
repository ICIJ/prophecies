<script>
import { formatDateLongAlt } from '@/utils/date'
import UserCard from '@/components/UserCard'
import AdminBadge from '@/components/AdminBadge'

export default {
  name: 'UserRetrieveProfile',
  components: {
    UserCard,
    AdminBadge
  },
  filters: {
    formatDate(d) {
      return formatDateLongAlt(d)
    }
  },
  props: {
    username: {
      type: String
    }
  }
}
</script>

<template>
  <user-card :username="username" class="user-retrieve-profile">
    <template #content="{ user }">
      <ul class="list-unstyled mt-5">
        <li v-if="user.isSuperuser" class="user-retrieve-profile__super-user mb-3">
          <admin-badge />
        </li>
        <li class="user-retrieve-profile__email mb-3">
          Email: <a v-if="user.email" :href="`mailto:${user.email}`">{{ user.email }}</a
          ><template v-else>{{ $t('userRetrieveProfile.notProvided') }}</template>
        </li>
        <li class="user-retrieve-profile__last-login">
          {{ $t('userRetrieveProfile.lastLogin') }}: {{ user.lastLogin | formatDate }}
        </li>
      </ul>
    </template>
  </user-card>
</template>
