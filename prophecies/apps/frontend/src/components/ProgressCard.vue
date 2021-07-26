<template>
  <div class="card card-body py-4 px-5 shadow">
    <div class="card-flex align-items-center mt-3 mb-5">
      <users-icon class="text-primary mr-4" />
      <b-btn-group>
        <b-btn variant="primary" class="font-weight-bold">
          Team progress
        </b-btn>
        <b-btn variant="outline-primary">
          Your progress
        </b-btn>
      </b-btn-group>
    </div>
    <ul class="list-unstyled">
      <li class="font-weight-bold">
        <div class="d-flex align-items-start">
          <div class="mr-4">
            22%
          </div>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="22" :max="100" class="mb-1" />
            all open tasks
          </div>
        </div>
      </li>
      <li>
        <div class="d-flex align-items-start">
          <div class="mr-4">
            29%
          </div>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="29" :max="100" class="mb-1" />
            SAR transactions
          </div>
        </div>
      </li>
      <li>
        <div class="d-flex align-items-start">
          <div class="mr-4">
            38%
          </div>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="38" :max="100" class="mb-1" />
            Addresses
          </div>
        </div>
      </li>
      <li>
        <div class="d-flex align-items-start">
          <div class="mr-4">
            10%
          </div>
          <div class="flex-grow-1 pt-1 pb-4">
            <b-progress :value="10" :max="100" class="mb-1" />
            Transactions' amounts
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
