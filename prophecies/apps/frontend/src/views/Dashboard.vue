<template>
  <div class="dashboard d-flex align-items-start">
    <app-sidebar class="w-100 sticky-top" />
    <div class="dashboard__container flex-grow-1">
      <app-header />
      <div class="container-fluid p-5">
        <div class="row">
          <div class="col-4 offset-1">
            <div class="d-flex align-items-center">
              <b-btn-group>
                <b-btn variant="primary" class="font-weight-bold">
                  Team stats
                </b-btn>
                <b-btn variant="outline-primary">
                  Your stats
                </b-btn>
              </b-btn-group>
              <b-dropdown right no-caret variant="link" class="ml-auto">
                <template #button-content>
                  Sort by
                  <chevron-down-icon class="mr-2" />
                </template>
              </b-dropdown>
            </div>
            <stats-card title="SAR transaction" project="Chronos" :priority="1" class="my-5" />
            <stats-card title="Addresses" project="Hemeras" :priority="1" class="my-5" />
            <stats-card title="Transactions' amounts" project="Pontus" :priority="2" class="my-5" />
            <stats-card title="Passports" project="Pontus" :priority="1" class="my-5" />
          </div>
          <div class="col-4 offset-2">
            <progress-card class="mb-5" />
            <latest-tips-card />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import AppSidebar from '@/components/AppSidebar'
import LatestTipsCard from '@/components/LatestTipsCard'
import ProgressCard from '@/components/ProgressCard'
import StatsCard from '@/components/StatsCard'

export default {
  name: 'Dashboard',
  components: {
    AppHeader,
    AppSidebar,
    LatestTipsCard,
    ProgressCard,
    StatsCard
  }
}
</script>
