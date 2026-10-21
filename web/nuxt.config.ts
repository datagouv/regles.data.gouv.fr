import type { RouteName } from './catalogue/routes'
import { fileURLToPath } from 'node:url'
import { routes } from './catalogue/routes'

const views: Record<RouteName, string> = {
  catalogue: 'CatalogueView.vue',
  record: 'RecordView.vue',
}

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
  // enable vue-router without scanning app/pages: catalogue/routes.ts declares the routes
  pages: { enabled: true, pattern: [] },
  hooks: {
    'pages:extend': function (pages) {
      for (const [name, path] of Object.entries(routes) as [RouteName, string][]) {
        pages.push({ name, path, file: fileURLToPath(new URL(`app/views/${views[name]}`, import.meta.url)) })
      }
    },
  },
  nitro: {
    serverAssets: [{ baseName: 'records', dir: fileURLToPath(new URL('../data', import.meta.url)) }],
    // no page links to the registry file, so the crawler does not find it
    prerender: { routes: ['/registry.json'] },
  },
})
