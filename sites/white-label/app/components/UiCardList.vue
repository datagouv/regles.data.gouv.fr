<script setup lang="ts">
import type { UiCardListProps } from '#layers/web/shared/types/ui'

defineProps<UiCardListProps>()
</script>

<template>
  <ul>
    <li
      v-for="card in cards"
      :key="card.to"
    >
      <h2>
        <NuxtLink :to="card.to">
          {{ card.title }}
        </NuxtLink>
      </h2>
      <p>
        {{ card.description }}
      </p>
    </li>
  </ul>
</template>
