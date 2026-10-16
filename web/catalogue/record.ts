import type { RegistryRecord } from '@datagouv/regles-core'
import { recordPath, routes } from './routes'

export interface RecordSummary {
  title: string
  description: string
  to: string
}

export interface CataloguePage {
  title: string
  cards: RecordSummary[]
}

export interface RecordDetail extends Omit<RecordSummary, 'to'> {
  breadcrumb: { links: { label: string, to: string }[], current: string }
  authority: string
  version: string
  validity: string | null
  source: { repository: string, commit: string | null } | null
  subjects: string[]
  updatedOn: string | null
}

const CATALOGUE_TITLE = 'Catalogue des règles'

const DATE_FORMAT = new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long', timeZone: 'UTC' })

export function toRecordSummary(record: RegistryRecord): RecordSummary {
  return {
    title: frenchText(record.title),
    description: frenchText(record.description),
    to: recordPath(record.identifier),
  }
}

export function toCataloguePage(records: RegistryRecord[]): CataloguePage {
  return {
    title: CATALOGUE_TITLE,
    cards: records.map(toRecordSummary),
  }
}

export function toRecordDetail(record: RegistryRecord): RecordDetail {
  const title = frenchText(record.title)
  return {
    title,
    description: frenchText(record.description),
    breadcrumb: { links: [{ label: CATALOGUE_TITLE, to: routes.catalogue }], current: title },
    authority: record.competent_authority,
    version: record.version,
    validity: describeValidity(record.valid_from, record.valid_to),
    source: record.source_repository === null
      ? null
      : { repository: record.source_repository, commit: record.source_commit?.slice(0, 7) ?? null },
    subjects: (record.subjects ?? []).filter(subject => typeof subject === 'string'),
    updatedOn: formatDate(record.updated_at ?? record.created_at),
  }
}

function frenchText(text: { [language: string]: unknown }): string {
  const value = text.fr ?? Object.values(text)[0]
  return typeof value === 'string'
    ? value
    : ''
}

function describeValidity(from: string | null, to: string | null): string | null {
  if (from && to) {
    return `Du ${formatDate(from)} au ${formatDate(to)}`
  }
  if (from) {
    return `Depuis le ${formatDate(from)}`
  }
  if (to) {
    return `Jusqu'au ${formatDate(to)}`
  }
  return null
}

function formatDate(date: string | null): string | null {
  // Intl writes the first day of a month as « 1 », French typography writes « 1er »
  return date === null
    ? null
    : DATE_FORMAT.format(new Date(date)).replace(/^1 /, '1er ')
}
