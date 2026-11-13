import { assert, describe, expect, it } from 'vitest'
import exampleRecord from '../fixtures/record.json' with { type: 'json' }
import { readRecord } from './record.ts'

describe('readRecord', () => {
  it('reads the record of a valid file', () => {
    const result = readRecord(exampleRecord)
    assert(result.valid)
    expect(result.record.identifier).toBe('prestagri-aide-scolarite')
    expect(result.record.valid_from).toBeNull()
  })

  it('reports an optional field missing from a record', () => {
    const { valid_from, ...incomplete } = exampleRecord
    expect(readRecord(incomplete)).toEqual(gaps('valid_from'))
  })

  it('reports a field outside the schema', () => {
    expect(readRecord({ ...exampleRecord, extra: 1 })).toEqual(gaps('extra'))
  })

  it('reports a value outside the format of its field', () => {
    expect(readRecord({ ...exampleRecord, id: 'not a uri' })).toEqual(gaps('id'))
  })

  it('reports the top-level field of a gap inside a nested object', () => {
    expect(readRecord({ ...exampleRecord, title: { en: 'School allowance calculation' } })).toEqual(gaps('title'))
  })

  it('reports a file that contains a list of records', () => {
    expect(readRecord([exampleRecord])).toEqual(gaps(null))
  })
})

function gaps(...fields: (string | null)[]) {
  return { valid: false, gaps: fields.map(field => expect.objectContaining({ field })) }
}
