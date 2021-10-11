<script>
import ShortcutListCard from '@/components/ShortcutListCard'

export default {
  name: 'App',
  components: {
    ShortcutListCard
  }
}
</script>

<template>
  <div class="app">
    <span v-shortkey="['ctrl', 'k']" @shortkey="$refs['modal-shortcuts'].toggle()">
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