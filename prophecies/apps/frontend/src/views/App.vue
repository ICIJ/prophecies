<script>
import ShortcutListCard from '@/components/ShortcutListCard'

export default {
  name: 'App',
  components: {
    ShortcutListCard
  },
  computed: {
    shortkeys () {
      return {
        toggleShortcuts: 'ctrl+k',
        goToTipList: 'ctrl+shift+t',
        goToHistory: 'ctrl+shift+h'
      }
    }
  },
  created () {
    this.$root.$on('prophecies::toggleShortcuts', this.toggleShortcuts)    
  },
  methods: {
    mapShortkeys ({ detail: { srcKey: method } }) {
      if (method in this.$options.methods) {
        this[method]()
      }
    },
    goTo (name) {
      if (this.$route.name !== name) {
        this.$router.push({ name })
      }
    },
    goToTipList () {
      this.goTo('tip-list')
    },
    goToHistory () {
      this.goTo('history')
    },
    toggleShortcuts () {
      this.$refs['modal-shortcuts'].toggle()
    }
  }
}
</script>

<template>
  <div class="app">
    <span v-shortkey="shortkeys" @shortkey="mapShortkeys($event)">
      <b-modal 
        size="md"
        content-class="bg-transparent shadow-none border-0" 
        body-class="p-0"
        ref="modal-shortcuts" 
        hide-footer 
        hide-header>
        <shortcut-list-card>
          <template #header>
            <b-btn class="float-right px-2" variant="link" @click="$refs['modal-shortcuts'].toggle()">
              <x-icon />
              <span class="sr-only">Close</span>
            </b-btn>
          </template>
        </shortcut-list-card>
      </b-modal>
    </span>
    <router-view />
  </div>
</template>