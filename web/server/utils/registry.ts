import type { Registry, RegistryGap } from '@datagouv/regles-core'
import { buildRegistry } from '@datagouv/regles-core'

export async function loadRegistry(): Promise<Registry> {
  const storage = useStorage('assets:records')
  const keys = (await storage.getKeys()).filter(key => key.endsWith('.json'))
  const files = await Promise.all(keys.map(async key => ({
    // unstorage separates the levels of a key with colons
    path: `data/${key.replaceAll(':', '/')}`,
    content: await storage.getItem(key),
  })))

  const result = buildRegistry(files)
  if (!result.valid) {
    throw createError({ statusCode: 500, statusMessage: `Invalid records: ${result.gaps.map(describeGap).join('; ')}` })
  }
  return result.registry
}

function describeGap(gap: RegistryGap): string {
  const location = [gap.path]
  if (gap.recordIndex !== null) {
    location.push(`record ${gap.recordIndex}`)
  }
  if (gap.field !== null) {
    location.push(gap.field)
  }
  return `${location.join(', ')}: ${gap.message}`
}
