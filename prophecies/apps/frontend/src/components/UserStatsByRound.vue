<template>
  <div class="user-stats-by-round d-flex flex-column p-3">
    <div class="user-stats-by-round__progress d-flex flex-row">
      Round 1
      <b-progress :value="10 | round" :max="100" />
    </div>
    <div class="user-stats-by-round__users d-flex flex-column">
      <div class="d-flex flex-row p-2" v-for="(user, index) in users" :key="index">
        <div class="">
          {{ user.name }}
        </div>
        <div>
          {{ user.progress }}%
        </div>
        <div>
          <check-icon size="1x" class="text-primary mr-2" />  {{user.done}}
        </div>
        <div>
          <clock-icon size="1x" class="text-danger mr-2" />  {{user.pending}}
        </div>
      </div>
    </div>
    <div class="user-stats-by-round__summary row">

    </div>
  </div>
</template>

<script>

export default {
  name: 'UserStatsByRound',
  props: {
  },
  filters: {
    round (value) {
      return Math.round(value)
    }
  },
  data () {
    return {
        users: [
          {
            name: 'augie',
            progress: 100,
            done: 5,
            pending: 0
          },
          {
            name: 'marco',
            progress: 0,
            done: 0,
            pending: 20
          },
          {
            name: 'mago',
            progress: 0,
            done: 0,
            pending: 30
          }
        ],
        summary: [
          {
            name: 'C',
            value: 95
          },
          {
            name: 'I',
            value: 1
          },
          {
            name: 'D',
            value: 4
          }
        ]
    }
  },
  computed: {

  }
}
</script>

<style lang="scss" scoped>

</style>
