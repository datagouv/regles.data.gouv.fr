<script setup lang="ts">
import { DsfrFooter, DsfrHeader, DsfrNavigation, DsfrSkipLinks } from '@gouvminint/vue-dsfr'
import { routes } from '#layers/web/routes'

const { siteName, navigation } = useAppConfig()
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
    :home-to="routes.catalogue"
    :logo-text="logoText"
  >
    <template #mainnav>
      <DsfrNavigation :nav-items="navigation" />
    </template>
  </DsfrHeader>
  <main
    id="content"
    tabindex="-1"
  >
    <slot />
  </main>
  <DsfrFooter
    id="footer"
    :home-link="routes.catalogue"
    :logo-text="logoText"
    :mandatory-links="[]"
  />
</template>
