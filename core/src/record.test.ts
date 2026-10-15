import { readFileSync } from 'node:fs'
import { assert, describe, expect, it } from 'vitest'
import { readRecords } from './record.ts'

const EXAMPLE_FILE = new URL('../../data/ministereAgriculture/prestagri/aideScolarite.json', import.meta.url)
const [exampleRecord] = JSON.parse(readFileSync(EXAMPLE_FILE, 'utf8'))

describe('readRecords', () => {
  it('reads the records of a valid file', () => {
    const result = readRecords([exampleRecord])
    assert(result.valid)
    expect(result.records[0].identifier).toBe('prestagri-aide-scolarite')
    expect(result.records[0].valid_from).toBeNull()
  })

  it('reports an optional field missing from a record', () => {
    const { valid_from, ...incomplete } = exampleRecord
    expect(readRecords([incomplete])).toEqual(gaps({ recordIndex: 0, field: 'valid_from' }))
  })

  it('reports a field outside the schema', () => {
    expect(readRecords([{ ...exampleRecord, extra: 1 }])).toEqual(gaps({ recordIndex: 0, field: 'extra' }))
  })

  it('reports a value outside the format of its field', () => {
    expect(readRecords([{ ...exampleRecord, id: 'not a uri' }])).toEqual(gaps({ recordIndex: 0, field: 'id' }))
  })

  it('reports a file that contains no list of records', () => {
    expect(readRecords(exampleRecord)).toEqual(gaps({ recordIndex: null, field: null }))
  })
})

function gaps(...expected: { recordIndex: number | null, field: string | null }[]) {
  return { valid: false, gaps: expected.map(gap => expect.objectContaining(gap)) }
}
