<script setup lang="ts">
import type { UiPageHeaderProps } from '#layers/web/shared/types/ui'

defineProps<UiPageHeaderProps>()
</script>

<template>
  <div class="page-header fr-background-alt--blue-france">
    <BrandWaves class="page-header-waves" />
    <div
      class="page-header-content fr-container fr-pb-6w"
      :class="{ 'fr-pt-6w': !breadcrumb }"
    >
      <UiBreadcrumb
        v-if="breadcrumb"
        v-bind="breadcrumb"
      />
      <h1 :class="{ 'fr-mb-0': !lead }">
        {{ title }}
      </h1>
      <p
        v-if="lead"
        class="fr-text--lead fr-mb-0"
      >
        {{ lead }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  position: relative;
}

.page-header-waves {
  opacity: 0.8;
  mix-blend-mode: darken;
}

.page-header-content {
  position: relative;
  /* keeps the margins of the DSFR breadcrumb inside the band */
  display: flow-root;
}
</style>
