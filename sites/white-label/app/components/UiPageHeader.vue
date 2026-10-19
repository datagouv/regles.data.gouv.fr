<script setup lang="ts">
import type { UiPageHeaderProps } from '#layers/web/shared/types/ui'

defineProps<UiPageHeaderProps>()
</script>

<template>
  <div class="page-header">
    <div class="page-header-content container">
      <UiBreadcrumb
        v-if="breadcrumb"
        v-bind="breadcrumb"
      />
      <h1>{{ title }}</h1>
      <p
        v-if="lead"
        class="page-header-lead"
      >
        {{ lead }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  background: var(--color-background-alt);
}

.page-header-content > :last-child {
  margin-bottom: 0;
}

.page-header-lead {
  font-size: var(--font-size-large);
}
</style>
