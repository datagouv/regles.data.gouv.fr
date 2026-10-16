<script setup lang="ts">
import type { UiBreadcrumbProps } from '#layers/web/shared/types/ui'

defineProps<UiBreadcrumbProps>()
</script>

<template>
  <nav
    aria-label="Vous êtes ici :"
  >
    <ol>
      <li
        v-for="link in links"
        :key="link.to"
      >
        <NuxtLink :to="link.to">
          {{ link.label }}
        </NuxtLink>
      </li>
      <li aria-current="page">
        {{ current }}
      </li>
    </ol>
  </nav>
</template>
