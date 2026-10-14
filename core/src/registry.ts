import type { RecordGap, RegistryRecord } from './record.ts'
import { UNIQUE_FIELDS } from './generated/unique-fields.ts'
import { readRecords } from './record.ts'

export interface RecordFile {
  path: string
  content: unknown
}

export interface RegistryGap extends RecordGap {
  path: string
}

export interface Registry {
  records: RegistryRecord[]
  find: (identifier: string) => RegistryRecord | undefined
}

export type BuildRegistryResult
  = | { valid: true, registry: Registry }
    | { valid: false, gaps: RegistryGap[] }

interface Entry {
  path: string
  recordIndex: number
  record: RegistryRecord
}

export function buildRegistry(files: RecordFile[]): BuildRegistryResult {
  const entries: Entry[] = []
  const gaps: RegistryGap[] = []

  for (const file of files) {
    const result = readRecords(file.content)
    if (result.valid) {
      entries.push(...result.records.map((record, recordIndex) => ({ path: file.path, recordIndex, record })))
    }
    else {
      gaps.push(...result.gaps.map(gap => ({ path: file.path, ...gap })))
    }
  }
  gaps.push(...UNIQUE_FIELDS.flatMap(field => findDuplicates(entries, field)))

  if (gaps.length > 0) {
    return { valid: false, gaps }
  }
  const byIdentifier = new Map(entries.map(entry => [entry.record.identifier, entry.record]))
  return {
    valid: true,
    registry: {
      records: entries.map(entry => entry.record),
      find: identifier => byIdentifier.get(identifier),
    },
  }
}

function findDuplicates(entries: Entry[], field: keyof RegistryRecord): RegistryGap[] {
  const firstEntries = new Map<string, Entry>()
  const gaps: RegistryGap[] = []

  for (const entry of entries) {
    if (entry.record[field] === null) {
      continue
    }
    const value = JSON.stringify(entry.record[field])
    const first = firstEntries.get(value)
    if (first) {
      gaps.push({
        path: entry.path,
        recordIndex: entry.recordIndex,
        field,
        message: `has the same ${field} as ${first.path}, record ${first.recordIndex}`,
      })
    }
    else {
      firstEntries.set(value, entry)
    }
  }
  return gaps
}
