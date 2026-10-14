import type { RegistryRecord } from '@datagouv/regles-core'
import { readRecords } from '@datagouv/regles-core'
import { assert, describe, expect, it } from 'vitest'
import exampleFile from '../../data/ministereAgriculture/prestagri/aideScolarite.json' with { type: 'json' }
import { toRecordDetail, toRecordSummary } from './record.ts'

const example = readRecords(exampleFile)
assert(example.valid)
const exampleRecord: RegistryRecord = example.records[0]!

describe('toRecordSummary', () => {
  it('shows the French title and description', () => {
    expect(toRecordSummary(exampleRecord)).toEqual({
      identifier: 'prestagri-aide-scolarite',
      title: 'Calcul de l\'aide à la scolarité',
      description: expect.stringMatching(/^Calcule le montant de l'aide à la scolarité/),
    })
  })

  it('falls back on the first language when the French text is missing', () => {
    const record = { ...exampleRecord, title: { en: 'School allowance calculation' } }
    expect(toRecordSummary(record).title).toBe('School allowance calculation')
  })
})

describe('toRecordDetail', () => {
  it.each([
    ['2026-01-01', '2026-12-31', 'Du 1er janvier 2026 au 31 décembre 2026'],
    ['2026-01-01', null, 'Depuis le 1er janvier 2026'],
    [null, '2026-12-31', 'Jusqu\'au 31 décembre 2026'],
    [null, null, null],
  ])('describes the validity from %s to %s', (validFrom, validTo, validity) => {
    expect(toRecordDetail({ ...exampleRecord, valid_from: validFrom, valid_to: validTo }).validity).toBe(validity)
  })

  it('shortens the source commit to seven characters', () => {
    expect(toRecordDetail(exampleRecord).source).toEqual({ repository: 'https://github.com/betagouv/prestagri', commit: '478b3cc' })
  })

  it('leaves out the source when the record has none', () => {
    expect(toRecordDetail({ ...exampleRecord, source_repository: null, source_commit: null }).source).toBeNull()
  })
})
