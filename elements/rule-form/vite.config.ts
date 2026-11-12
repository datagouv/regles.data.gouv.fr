import { fileURLToPath } from 'node:url'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  publicDir: false,
  define: { 'process.env.NODE_ENV': '"production"' },
  resolve: {
    dedupe: ['vue'],
    // the component imports the web layer by the alias that Nuxt generates for its sites
    alias: { '#layers/web': fileURLToPath(new URL('node_modules/@datagouv/regles-web', import.meta.url)) },
  },
  build: {
    lib: {
      entry: fileURLToPath(new URL('rule-form.ts', import.meta.url)),
      formats: ['es'],
      fileName: () => 'rule-form.js',
      cssFileName: 'rule-form',
    },
  },
})
