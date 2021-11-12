<script>
import ShortcutListCard from '@/components/ShortcutListCard'
import TipListCard from '@/components/TipListCard'

export default {
  name: 'App',
  components: {
    ShortcutListCard,
    TipListCard
  },
  computed: {
    taskId () {
      return this.$route.params.taskId || null
    }
  },
  created () {
    this.$root.$on('prophecies::toggleShortcuts', this.toggleModalFn('modal-shortcuts')) 
    this.$root.$on('prophecies::toggleTips', this.toggleModalFn('modal-tips'))  
    this.$shortkey.bind('ctrl+k', this.toggleModalFn('modal-shortcuts')) 
    this.$shortkey.bind('ctrl+shift+t', this.toggleModalFn('modal-tips')) 
    this.$shortkey.bind('ctrl+shift+h', this.goToHistory) 
  },
  methods: {
    goTo (name) {
      if (this.$route.name !== name) {
        this.$router.push({ name })
      }
    },
    goToHistory () {
      this.goTo('history')
    },
    toggleModalFn (modalRef) {
      return (event) => {
        event.preventDefault()
        this.$refs[modalRef].toggle()
      }
    }
  }
}
</script>

<template>
  <div class="app">
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
    <b-modal 
      size="md"
      content-class="bg-transparent shadow-none border-0" 
      body-class="p-0"
      ref="modal-tips" 
      hide-footer 
      hide-header>
      <tip-list-card :query="{ 'filter[task]': taskId }">
        <template #header>
          <b-btn class="float-right px-2" variant="link" @click="$refs['modal-tips'].toggle()">
            <x-icon />
            <span class="sr-only">Close</span>
          </b-btn>
        </template>
      </tip-list-card>
    </b-modal>
    <router-view />
  </div>
</template>
