import { fileURLToPath } from 'node:url'

export default defineNuxtConfig({
  $meta: { name: 'web' },
  compatibilityDate: '2026-10-01',
  app: {
    head: {
      htmlAttrs: { lang: 'fr' },
    },
  },
  typescript: {
    // vue-tsc accepts an unknown component by default, so a site missing a UI component would pass
    tsConfig: { vueCompilerOptions: { checkUnknownComponents: true } },
    // the shared project declares no Vue auto-import, so nuxt typecheck rejects a Vue global in the catalogue
    sharedTsConfig: { include: [fileURLToPath(new URL('catalogue/**/*', import.meta.url))] },
  },
  // enable vue-router without scanning app/pages: modules/view-routes.ts adds the routes of each layer
  pages: { enabled: true, pattern: [] },
  nitro: {
    serverAssets: [{ baseName: 'records', dir: fileURLToPath(new URL('../data', import.meta.url)) }],
    // no page links to the registry file, so the crawler does not find it
    prerender: { routes: ['/registry.json'] },
  },
})
