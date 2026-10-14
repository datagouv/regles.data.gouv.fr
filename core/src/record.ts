import type { ErrorObject } from 'ajv'
import type { RegistryRecord } from './generated/record.ts'
import { Ajv } from 'ajv'
import ajvFormats from 'ajv-formats'
import recordSchema from './generated/record.schema.json' with { type: 'json' }

export type { RegistryRecord }

export interface RecordGap {
  recordIndex: number | null
  field: string | null
  message: string
}

export type ReadRecordsResult
  = | { valid: true, records: RegistryRecord[] }
    | { valid: false, gaps: RecordGap[] }

const ajv = new Ajv({ allErrors: true })
ajvFormats.default(ajv)
const validateRecords = ajv.compile<RegistryRecord[]>({ type: 'array', items: recordSchema })

export function readRecords(content: unknown): ReadRecordsResult {
  if (validateRecords(content)) {
    return { valid: true, records: content }
  }
  return { valid: false, gaps: (validateRecords.errors ?? []).map(toRecordGap) }
}

function toRecordGap(error: ErrorObject): RecordGap {
  const [recordIndex, field] = error.instancePath.split('/').slice(1)
  return {
    recordIndex: recordIndex === undefined
      ? null
      : Number(recordIndex),
    field: field ?? error.params.missingProperty ?? error.params.additionalProperty ?? null,
    message: error.message ?? error.keyword,
  }
}
