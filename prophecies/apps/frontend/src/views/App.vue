<script>
import ShortcutListCard from '@/components/ShortcutListCard'
import TipListCard from '@/components/TipListCard'

export default {
  name: 'App',
  components: {
    ShortcutListCard,
    TipListCard
  },
  async created() {
    if (await this.$core.getUser()) {
      // Bind root events
      this.$root.$on('prophecies::closeTips', this.closeTips)
      this.$root.$on('prophecies::toggleShortcuts', this.toggleModalFn('modal-shortcuts'))
      this.$root.$on('prophecies::toggleTips', this.toggleModalFn('modal-tips'))
      // Bind keyboard shortcuts
      this.$shortkey.bind('ctrl+k', this.toggleModalFn('modal-shortcuts'))
      this.$shortkey.bind('ctrl+shift+i', this.toggleModalFn('modal-tips'))
      this.$shortkey.bind('ctrl+shift+h', this.goToHistory)
    }
  },
  methods: {
    goTo(name) {
      if (this.$route.name !== name) {
        this.$router.push({ name })
      }
    },
    goToHistory() {
      this.goTo('history')
    },
    toggleModalFn(modalRef) {
      return (event = null) => {
        if (event) {
          event.preventDefault()
        }
        this.$refs[modalRef].toggle()
      }
    },
    closeTips() {
      this.$bvModal.hide('modal-tips')
      this.goTo('tip-list')
    }
  }
}
</script>

<template>
  <div class="app">
    <b-modal
      ref="modal-shortcuts"
      size="md"
      content-class="bg-transparent shadow-none border-0"
      body-class="p-0"
      hide-footer
      hide-header
    >
      <shortcut-list-card>
        <template #header>
          <b-btn class="float-right px-2" variant="link" @click="$refs['modal-shortcuts'].toggle()">
            <x-icon />
            <span class="sr-only">{{ $t('app.close') }}</span>
          </b-btn>
        </template>
      </shortcut-list-card>
    </b-modal>
    <b-modal
      id="modal-tips"
      ref="modal-tips"
      size="md"
      content-class="bg-transparent shadow-none border-0"
      body-class="p-0"
      hide-footer
      hide-header
    >
      <tip-list-card>
        <template #header>
          <b-btn class="float-right px-2" variant="link" @click="$refs['modal-tips'].toggle()">
            <x-icon />
            <span class="sr-only">{{ $t('app.close') }}</span>
          </b-btn>
        </template>
      </tip-list-card>
    </b-modal>
    <router-view />
  </div>
</template>

<style lang="scss">
.app {
  &__breadcrumb {
    display: inline-flex;
    align-items: center;
    margin-left: 2.6rem;
    text-decoration: underline;
    text-decoration-color: $warning;
    text-decoration-thickness: 7px;
    text-underline-offset: 5px;
    line-height: 24px;

    &:after {
      content: '\00a0\00a0';
    }

    &__item--dashboard svg {
      transform: translateY(-0.2em);
    }

    &__item.list-inline-item {
      font-size: $font-size-lg;
      margin-right: 0;
      display: inline-flex;
      align-items: center;
      font-weight: 600;
    }
  }
}
</style>
