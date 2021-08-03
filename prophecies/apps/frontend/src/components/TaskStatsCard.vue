<template>
  <div class="card card-body shadow d-flex">
    <div></div>
    <div>
      <div class="d-flex align-items-center mb-3">
        <h3 class="m-0">
          {{ task.name }}
          <b-badge class="bg-transparent font-weight-normal text-muted">
            {{ task.project.name }}
          </b-badge>
        </h3>
        <span class="bg-warning rounded py-1 px-2 ml-auto">
          Priority {{ task.priority }}
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
          <li class="list-inline-item" v-for="round in task.rounds" :key="round">
            Round {{ round }}
            <span class="font-weight-bold ml-3">
              {{ task.user_progress_by_round[round] }}%
            </span>
            <span class="text-muted mx-2" v-if="round !== task.rounds">
              |
            </span>
          </li>
        </ul>
        <span class="bg-primary text-white font-weight-bold rounded py-1 px-2 ml-auto">
          {{ task.progress }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import Task from '@/models/Task'
export default {
  name: 'StatsCard',
  props: {
    taskId: {
      type: Number
    }
  },
  computed: {
    task () {
      return Task
        .query()
        .with('project')
        .with('choice_group')
        .with('choice_group.choices')
        .find(this.taskId)
    }
  }
}
</script>
