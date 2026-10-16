<script setup lang="ts">
import type { UiBreadcrumbProps } from '#layers/web/shared/types/ui'
import { DsfrBreadcrumb } from '@gouvminint/vue-dsfr'

const props = defineProps<UiBreadcrumbProps>()

const links = computed(() => [
  ...props.links.map(link => ({ text: link.label, to: link.to })),
  { text: props.current },
])
</script>

<template>
  <DsfrBreadcrumb :links="links" />
</template>
