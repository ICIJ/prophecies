<template>
    <div class="tip-list-card p-3">
        <app-waiter :loader="fetchFilteredTipsLoader" waiter-class="my-5 mx-auto d-block">
            <slot name="header" />
            <div class="tip-list-card__content pt-5 pb-0">
                <b-list-group-item v-for="{ id } in tips" class="flex-column align-items-start ml-4 border-0" :key="id">
                    <tip-card :tip-id="id" />
                </b-list-group-item>
            </div>
        </app-waiter>
    </div>
</template>

<script>
import { uniqueId } from 'lodash'
import AppWaiter from '@/components/AppWaiter'
import Tip from '@/models/Tip'
import TipCard from '@/components/TipCard'

export default {
    name: 'TipListCard',
    components: {
        AppWaiter,
        TipCard
    },
    props: {
        query: {
            type: Object,
            default: () => ({
                'filter[task]': null
            })
        }
    },
    data () {
        return {
            taskFilter: 'filter[task]'
        }
    },
    created () {
        return this.setup()
    },
    computed: {
        fetchFilteredTipsLoader () {
            return uniqueId('load-filtered-tips-')
        },
        tips () {
            return Tip.query()
                .with('project')
                .with('task')
                .where(({ taskId }) => {
                    return !this.query['filter[task]'] || taskId === this.query['filter[task]']
                })
                .get()
        }
    },
    methods: {
        async setup () {
            try {
                this.$wait.start(this.fetchFilteredTipsLoader)
                await this.fetchTips()
                this.$wait.end(this.fetchFilteredTipsLoader)
            } catch (error) {
                const title = 'Unable to retrieve tips'
                this.$router.replace({ name: 'error', params: { title, error } })
            }
        },
        fetchTips () {
            return Tip.api().get()
        }
    }
}
</script>

<style lang="scss" scoped>
    @keyframes highlightRow {
        from {
            background: #fcf3c4;
        }
        to {
            background: $primary-10;
        }
    }

  .tip-list-card {
    background-color: $primary-10;
    border-radius: $card-border-radius;
  }
</style>