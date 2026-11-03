import { existsSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineNuxtModule } from 'nuxt/kit'

export interface RecordsOptions {
  // Folder of the record files, relative to the project that generates the site
  dir: string
}

export default defineNuxtModule<RecordsOptions>({
  meta: { name: 'records', configKey: 'records' },
  defaults: { dir: fileURLToPath(new URL('../../data', import.meta.url)) },
  setup(options, nuxt) {
    const dir = resolveRecordsDir(nuxt.options.rootDir, options.dir)
    nuxt.options.nitro.serverAssets = [...nuxt.options.nitro.serverAssets ?? [], { baseName: 'records', dir }]
  },
})

export function resolveRecordsDir(rootDir: string, dir: string): string {
  const resolved = resolve(rootDir, dir)
  if (!existsSync(resolved)) {
    throw new Error(`The record folder ${resolved} does not exist, set records.dir in nuxt.config.ts`)
  }
  return resolved
}
