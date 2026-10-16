<script setup lang="ts">
import type { UiBreadcrumbProps } from '#layers/web/shared/types/ui'

defineProps<UiBreadcrumbProps>()
</script>

<template>
  <nav
    class="breadcrumb"
    aria-label="Vous êtes ici :"
  >
    <ol class="breadcrumb-list">
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

<style scoped>
.breadcrumb {
  margin-bottom: var(--space-3);
  font-size: var(--font-size-small);
}

.breadcrumb-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin: 0;
  padding: 0;
  list-style: none;
}

.breadcrumb-list li + li::before {
  content: "›";
  margin-right: var(--space-1);
  color: var(--color-text-muted);
}
</style>
