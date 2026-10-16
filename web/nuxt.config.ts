export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  app: {
    head: {
      htmlAttrs: { lang: 'fr' },
    },
  },
  typescript: {
    // the shared project declares no Vue auto-import, so nuxt typecheck rejects a Vue global in the catalogue
    sharedTsConfig: { include: ['../catalogue/**/*'] },
  },
  nitro: {
    serverAssets: [{ baseName: 'records', dir: '../../data' }],
  },
})
