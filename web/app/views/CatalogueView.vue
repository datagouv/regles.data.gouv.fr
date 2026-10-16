<script setup lang="ts">
const { data: summaries, error } = await useFetch('/api/records')
if (error.value) {
  throw createError({ ...error.value, fatal: true })
}

useHead({ title: 'Catalogue des règles' })
</script>

<template>
  <div>
    <h1>Catalogue des règles</h1>
    <ul>
      <li v-for="summary in summaries" :key="summary.to">
        <h2>
          <NuxtLink :to="summary.to">
            {{ summary.title }}
          </NuxtLink>
        </h2>
        <p>{{ summary.description }}</p>
      </li>
    </ul>
  </div>
</template>
