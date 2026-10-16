import { toRecordSummary } from '../../../catalogue/record'

export default defineEventHandler(async () => {
  return (await loadRegistry()).records.map(toRecordSummary)
})
