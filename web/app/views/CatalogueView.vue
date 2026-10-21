<script setup lang="ts">
const { data: catalogue, error } = await useFetch('/api/records')
if (error.value || !catalogue.value) {
  throw createError({ ...error.value, fatal: true })
}

useHead({ title: catalogue.value.title })
</script>

<template>
  <template v-if="catalogue">
    <UiPageHeader :title="catalogue.title" />
    <UiPageBody>
      <UiCardList :cards="catalogue.cards" />
    </UiPageBody>
  </template>
</template>
