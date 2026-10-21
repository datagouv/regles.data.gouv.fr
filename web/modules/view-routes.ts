import type { NuxtPage } from 'nuxt/schema'
import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { defineNuxtModule, extendPages, getLayerDirectories } from 'nuxt/kit'

interface LayerRoutes {
  source: string
  app: string
  routes: Record<string, string>
}

export default defineNuxtModule({
  meta: { name: 'view-routes' },
  async setup() {
    const pages = await readLayerPages(getLayerDirectories())
    extendPages((existing) => {
      existing.push(...pages)
    })
  },
})

export async function readLayerPages(directories: { root: string, app: string }[]): Promise<NuxtPage[]> {
  return toPages(await readLayerRoutes(directories))
}

// getLayerDirectories lists the project first: reading the extended layers first makes an error name the layer that redeclares a route
async function readLayerRoutes(directories: { root: string, app: string }[]): Promise<LayerRoutes[]> {
  const layers: LayerRoutes[] = []
  for (const { root, app } of directories.toReversed()) {
    const source = join(root, 'routes.ts')
    if (existsSync(source)) {
      const { routes }: { routes?: Record<string, string> } = await import(pathToFileURL(source).href)
      if (!routes) {
        throw new Error(`${source} exports no routes`)
      }
      layers.push({ source, app, routes })
    }
  }
  return layers
}

function toPages(layers: LayerRoutes[]): NuxtPage[] {
  const sources = new Map<NuxtPage, string>()
  for (const { source, app, routes } of layers) {
    for (const [name, path] of Object.entries(routes)) {
      const file = join(app, 'views', `${name[0]!.toUpperCase()}${name.slice(1)}View.vue`)
      const taken = [...sources.keys()].find(page => page.name === name || page.path === path)
      if (taken) {
        throw new Error(`${source} declares the route ${name} at ${path}, already declared by ${sources.get(taken)} as ${String(taken.name)} at ${taken.path}`)
      }
      sources.set({ name, path, file }, source)
    }
  }
  return [...sources.keys()]
}
