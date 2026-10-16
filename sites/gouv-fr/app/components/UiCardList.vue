<script setup lang="ts">
import type { UiCardListProps } from '#layers/web/shared/types/ui'
import { DsfrCard } from '@gouvminint/vue-dsfr'

defineProps<UiCardListProps>()
</script>

<template>
  <ul class="fr-raw-list fr-grid-row fr-grid-row--gutters">
    <li
      v-for="card in cards"
      :key="card.to"
      class="fr-col-12 fr-col-md-6"
    >
      <DsfrCard
        :title="card.title"
        :description="card.description"
        :link="card.to"
        title-tag="h2"
      />
    </li>
  </ul>
</template>
