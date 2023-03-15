<script>
export default {
  name: 'AdminBadge'
}
</script>

<template>
    <span class="admin-badge d-inline-flex py-0 px-3 bg-warning rounded align-items-center text-primary">
            <award-icon size="1.5x" class="my-2 mr-2" />
            {{$t('adminBadge.admin')}}
          </span>
</template>
