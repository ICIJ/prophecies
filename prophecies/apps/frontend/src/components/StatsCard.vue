<template>
  <div class="card card-body shadow d-flex">
    <div></div>
    <div>
      <div class="d-flex align-items-center mb-3">
        <h3 class="m-0">
          {{ title }}
          <b-badge class="bg-transparent font-weight-normal text-muted">
            {{ project }}
          </b-badge>
        </h3>
        <span class="bg-warning rounded py-1 px-2 ml-auto">
          Priority {{ priority }}
        </span>
      </div>
      <p>
        Fully checked items:
        <span class="text-danger font-weight-bold ml-2">
          0 / 55
        </span>
      </p>
      <div class="d-flex align-items-center">
        <ul class="list-inline m-0">
          <li class="list-inline-item">
            Round 1
            <span class="font-weight-bold ml-3">
              77%
            </span>
            <span class="text-muted mx-2">
              |
            </span>
          </li>
          <li class="list-inline-item">
            Round 2
            <span class="font-weight-bold ml-3">
              10%
            </span>
            <span class="text-muted mx-2">
              |
            </span>
          </li>
          <li class="list-inline-item">
            Round 3
            <span class="font-weight-bold ml-3">
              0%
            </span>
          </li>
        </ul>
        <span class="bg-primary text-white font-weight-bold rounded py-1 px-2 ml-auto">
          29%
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsCard',
  props: {
    title: {
      type: String
    },
    priority: {
      type: Number
    },
    project: {
      type: String
    }
  }
}
</script>
