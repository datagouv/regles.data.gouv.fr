<script setup lang="ts">
import { DsfrFooter, DsfrHeader, DsfrSkipLinks } from '@gouvminint/vue-dsfr'

const { siteName } = useAppConfig()
const logoText = ['République', 'Française']
const skipLinks = [
  { id: 'content', text: 'Accéder au contenu' },
  { id: 'footer', text: 'Accéder au pied de page' },
]
</script>

<template>
  <DsfrSkipLinks :links="skipLinks" />
  <DsfrHeader
    :service-title="siteName"
    service-description="Règles publiques modélisées, ouvertes et réutilisables"
    home-to="/"
    :logo-text="logoText"
  />
  <main
    id="content"
    class="fr-container fr-py-6w"
    tabindex="-1"
  >
    <slot />
  </main>
  <DsfrFooter
    id="footer"
    :logo-text="logoText"
    :mandatory-links="[]"
  />
</template>
