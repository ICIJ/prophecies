<template>
  <div class="user-stats-by-round d-flex flex-column">
    <div class="user-stats-by-round__progress row">
      Round 1
      <b-progress :value="10 | round" :max="100" />
    </div>
    <div class="user-stats-by-round__users row">
      <div class="row" v-for="user in users">
        {{ user.name }}
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
