import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { resolveRecordsDir } from './records.ts'

const root = fileURLToPath(new URL('../', import.meta.url))

describe('resolveRecordsDir', () => {
  it('resolves the record folder from the project that generates the site', () => {
    expect(resolveRecordsDir(root, '../data')).toBe(fileURLToPath(new URL('../../data', import.meta.url)))
  })

  it('rejects a record folder that does not exist, and names it', () => {
    expect(() => resolveRecordsDir(root, 'missing')).toThrow(/web\/missing does not exist, set records\.dir in nuxt\.config\.ts$/)
  })
})
