import type { DsfrNavigationMenuLinkProps } from '@gouvminint/vue-dsfr'

declare module 'nuxt/schema' {
  interface AppConfigInput {
    navigation?: DsfrNavigationMenuLinkProps[]
  }
}

export {}
