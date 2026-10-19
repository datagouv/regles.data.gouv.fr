<script setup lang="ts">
import { DsfrFooter, DsfrHeader, DsfrSkipLinks } from '@gouvminint/vue-dsfr'
import { routes, routeTitles } from '~~/routes'

const { siteName } = useAppConfig()
const logoText = ['République', 'Française']
const quickLinks = [{ label: routeTitles.reference, to: routes.reference }]
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
    :quick-links="quickLinks"
  />
  <main
    id="content"
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
