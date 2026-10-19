<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{ error: NuxtError }>()

const title = computed(() => props.error.status === 404
  ? 'Page non trouvée'
  : 'Erreur inattendue')

useHead({ title })
</script>

<template>
  <SiteLayout>
    <UiPageHeader :title="title" />
    <UiPageBody>
      <p>Erreur {{ error.status }}</p>
      <NuxtLink to="/">
        Page d'accueil
      </NuxtLink>
    </UiPageBody>
  </SiteLayout>
</template>
