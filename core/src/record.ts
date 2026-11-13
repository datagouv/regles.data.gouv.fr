import type { ErrorObject } from 'ajv'
import type { RegistryRecord } from './generated/record.ts'
import ajvFormats from 'ajv-formats'
import { Ajv2020 } from 'ajv/dist/2020.js'
import recordSchema from './generated/record.schema.json' with { type: 'json' }

export type { RegistryRecord }

export interface RecordGap {
  field: string | null
  message: string
}

export type ReadRecordResult
  = | { valid: true, record: RegistryRecord }
    | { valid: false, gaps: RecordGap[] }

const ajv = new Ajv2020({ allErrors: true })
ajvFormats.default(ajv)
const validateRecord = ajv.compile<RegistryRecord>(recordSchema)

export function readRecord(content: unknown): ReadRecordResult {
  if (validateRecord(content)) {
    return { valid: true, record: content }
  }
  return {
    valid: false,
    gaps: (validateRecord.errors ?? []).map(toRecordGap),
  }
}

function toRecordGap(error: ErrorObject): RecordGap {
  const [field] = error.instancePath.split('/').slice(1)
  return {
    field: field ?? error.params.missingProperty ?? error.params.additionalProperty ?? null,
    message: error.message ?? error.keyword,
  }
}
