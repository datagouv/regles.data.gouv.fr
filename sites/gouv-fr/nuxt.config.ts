export default defineNuxtConfig({
  $meta: { name: 'gouv-fr' },
  extends: ['@datagouv/regles-web'],
  css: [
    '@gouvfr/dsfr/dist/core/core.main.min.css',
    '@gouvfr/dsfr/dist/component/component.main.min.css',
    '@gouvfr/dsfr/dist/utility/utility.main.min.css',
    '@gouvminint/vue-dsfr/styles',
  ],
})
