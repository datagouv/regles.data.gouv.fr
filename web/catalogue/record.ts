import type { RegistryRecord } from '@datagouv/regles-core'
import type { UiBreadcrumbProps, UiCard } from '../shared/types/ui'
import { recordPath, routes } from '../routes'

export interface CataloguePage {
  title: string
  cards: UiCard[]
}

export interface ExternalLink {
  label: string
  href: string | null
}

export interface RecordDetail {
  title: string
  description: string
  breadcrumb: UiBreadcrumbProps
  authority: ExternalLink
  version: string
  validity: string | null
  source: { repository: ExternalLink, commit: string | null } | null
  subjects: string[]
  updatedOn: string | null
}

const CATALOGUE_TITLE = 'Catalogue des règles'

const WEB_PROTOCOLS = new Set(['http:', 'https:'])

const DATE_FORMAT = new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long', timeZone: 'UTC' })

export function toRecordCard(record: RegistryRecord): UiCard {
  return {
    title: frenchText(record.title),
    description: frenchText(record.description),
    to: recordPath(record.identifier),
  }
}

export function toCataloguePage(records: RegistryRecord[]): CataloguePage {
  return {
    title: CATALOGUE_TITLE,
    cards: records.map(toRecordCard),
  }
}

export function toRecordDetail(record: RegistryRecord): RecordDetail {
  const title = frenchText(record.title)
  return {
    title,
    description: frenchText(record.description),
    breadcrumb: catalogueBreadcrumb(title),
    authority: externalLink(record.competent_authority),
    version: record.version,
    validity: describeValidity(record.valid_from, record.valid_to),
    source: record.source_repository === null
      ? null
      : { repository: externalLink(record.source_repository), commit: record.source_commit?.slice(0, 7) ?? null },
    subjects: (record.subjects ?? []).filter(subject => typeof subject === 'string'),
    updatedOn: formatDate(record.updated_at ?? record.created_at),
  }
}

export function catalogueBreadcrumb(current: string): UiBreadcrumbProps {
  return { links: [{ label: CATALOGUE_TITLE, to: routes.catalogue }], current }
}

function frenchText(text: { [language: string]: unknown }): string {
  const value = text.fr ?? Object.values(text)[0]
  return typeof value === 'string'
    ? value
    : ''
}

// the schema accepts any URI scheme, javascript: included, so only web addresses become links
function externalLink(url: string): ExternalLink {
  const href = WEB_PROTOCOLS.has(URL.parse(url)?.protocol ?? '')
    ? url
    : null
  return { label: url, href }
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
