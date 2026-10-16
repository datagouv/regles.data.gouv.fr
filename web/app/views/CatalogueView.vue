<script setup lang="ts">
const { data: catalogue, error } = await useFetch('/api/records')
if (error.value || !catalogue.value) {
  throw createError({ ...error.value, fatal: true })
}

useHead({ title: catalogue.value.title })
</script>

<template>
  <div v-if="catalogue">
    <h1>{{ catalogue.title }}</h1>
    <UiCardList :cards="catalogue.cards" />
  </div>
</template>
