import { assert, describe, expect, it } from 'vitest'
import { EXAMPLE_CONTENT, EXAMPLE_PATH, exampleRecord } from './example-record.ts'
import { buildRegistry } from './registry.ts'

describe('buildRegistry', () => {
  it('lists the records of every file and finds a record by its identifier', () => {
    const otherRecord = { ...exampleRecord, id: 'https://regles.data.gouv.fr/regles/autre', identifier: 'autre' }
    const result = buildRegistry([
      { path: EXAMPLE_PATH, content: EXAMPLE_CONTENT },
      { path: 'data/autre.json', content: [otherRecord] },
    ])
    assert(result.valid)
    expect(result.registry.records.map(record => record.identifier)).toEqual(['prestagri-aide-scolarite', 'autre'])
    expect(result.registry.find('autre')?.id).toBe('https://regles.data.gouv.fr/regles/autre')
  })

  it('reports the file of an invalid record', () => {
    const { competent_authority, ...incomplete } = exampleRecord
    expect(buildRegistry([{ path: 'data/incomplete.json', content: [incomplete] }])).toEqual({
      valid: false,
      gaps: [expect.objectContaining({ path: 'data/incomplete.json', recordIndex: 0, field: 'competent_authority' })],
    })
  })

  it('reports a record that repeats the id and the identifier of another file', () => {
    expect(buildRegistry([
      { path: EXAMPLE_PATH, content: EXAMPLE_CONTENT },
      { path: 'data/copie.json', content: EXAMPLE_CONTENT },
    ])).toEqual({
      valid: false,
      gaps: [
        { path: 'data/copie.json', recordIndex: 0, field: 'id', message: `has the same id as ${EXAMPLE_PATH}, record 0` },
        { path: 'data/copie.json', recordIndex: 0, field: 'identifier', message: `has the same identifier as ${EXAMPLE_PATH}, record 0` },
      ],
    })
  })
})
