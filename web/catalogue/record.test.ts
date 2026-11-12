import type { RegistryRecord } from '@datagouv/regles-core'
import { describe, expect, it } from 'vitest'
import { toCataloguePage, toRecordCard, toRecordDetail } from './record.ts'

const exampleRecord: RegistryRecord = {
  id: 'https://regles.data.gouv.fr/regles/ministere-agriculture/prestagri-aide-scolarite',
  identifier: 'prestagri-aide-scolarite',
  version: '0.1.0',
  title: { fr: 'Calcul de l\'aide à la scolarité', en: 'School allowance calculation' },
  description: { fr: 'Calcule le montant de l\'aide à la scolarité à partir du quotient familial du foyer.' },
  valid_from: null,
  valid_to: null,
  subjects: null,
  source_repository: 'https://github.com/betagouv/prestagri',
  source_commit: '478b3cc2ab28299c73b94fdd192b0559ae5873b8',
  created_at: null,
  updated_at: null,
  competent_authority: 'https://github.com/betagouv/prestagri#organisation',
}

describe('toRecordCard', () => {
  it('shows the French title and description, and links to the record', () => {
    expect(toRecordCard(exampleRecord)).toEqual({
      title: 'Calcul de l\'aide à la scolarité',
      description: expect.stringMatching(/^Calcule le montant de l'aide à la scolarité/),
      to: '/regles/prestagri-aide-scolarite',
    })
  })

  it('falls back on the first language when the French text is missing', () => {
    const record = { ...exampleRecord, title: { en: 'School allowance calculation' } }
    expect(toRecordCard(record).title).toBe('School allowance calculation')
  })
})

describe('toCataloguePage', () => {
  it('titles the catalogue and shows a card per record', () => {
    expect(toCataloguePage([exampleRecord])).toEqual({
      title: 'Catalogue des règles',
      cards: [toRecordCard(exampleRecord)],
    })
  })
})

describe('toRecordDetail', () => {
  it('shows the French title and description', () => {
    expect(toRecordDetail(exampleRecord)).toMatchObject({
      title: 'Calcul de l\'aide à la scolarité',
      description: expect.stringMatching(/^Calcule le montant de l'aide à la scolarité/),
    })
  })

  it('leads back to the catalogue in the breadcrumb', () => {
    expect(toRecordDetail(exampleRecord).breadcrumb).toEqual({
      links: [{ label: 'Catalogue des règles', to: '/' }],
      current: 'Calcul de l\'aide à la scolarité',
    })
  })

  it.each([
    ['2026-01-01', '2026-12-31', 'Du 1er janvier 2026 au 31 décembre 2026'],
    ['2026-01-01', null, 'Depuis le 1er janvier 2026'],
    [null, '2026-12-31', 'Jusqu\'au 31 décembre 2026'],
    [null, null, null],
  ])('describes the validity from %s to %s', (validFrom, validTo, validity) => {
    expect(toRecordDetail({ ...exampleRecord, valid_from: validFrom, valid_to: validTo }).validity).toBe(validity)
  })

  it('shortens the source commit to seven characters', () => {
    expect(toRecordDetail(exampleRecord).source).toEqual({
      repository: { label: 'https://github.com/betagouv/prestagri', href: 'https://github.com/betagouv/prestagri' },
      commit: '478b3cc',
    })
  })

  it('leaves out the source when the record has none', () => {
    expect(toRecordDetail({ ...exampleRecord, source_repository: null, source_commit: null }).source).toBeNull()
  })

  it.each([
    'javascript:alert(1)',
    'data:text/html,test',
    'not a url',
  ])('shows %s as text, without a link', (url) => {
    const detail = toRecordDetail({ ...exampleRecord, competent_authority: url, source_repository: url })
    expect(detail.authority).toEqual({ label: url, href: null })
    expect(detail.source?.repository).toEqual({ label: url, href: null })
  })
})
