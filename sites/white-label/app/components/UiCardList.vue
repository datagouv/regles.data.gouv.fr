<script setup lang="ts">
import type { UiCardListProps } from '#layers/web/shared/types/ui'

defineProps<UiCardListProps>()
</script>

<template>
  <ul class="card-list">
    <li
      v-for="card in cards"
      :key="card.to"
      class="card"
    >
      <h2 class="card-title">
        <NuxtLink :to="card.to">
          {{ card.title }}
        </NuxtLink>
      </h2>
      <p class="card-description">
        {{ card.description }}
      </p>
    </li>
  </ul>
</template>

<style scoped>
.card-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 22rem), 1fr));
  gap: var(--space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.card {
  padding: var(--space-3);
  border: 1px solid var(--color-border);
}

.card-title {
  margin: 0 0 var(--space-1);
  font-size: var(--font-size-large);
}

.card-description {
  margin: 0;
  color: var(--color-text-muted);
}
</style>
