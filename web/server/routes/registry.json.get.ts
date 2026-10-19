import { SCHEMA_VERSION } from '@datagouv/regles-core'

export default defineEventHandler(async () => {
  return { schema_version: SCHEMA_VERSION, records: (await loadRegistry()).records }
})
