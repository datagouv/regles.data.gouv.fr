import { toRecordDetail } from '../../../catalogue/record'

export default defineEventHandler(async (event) => {
  const record = (await loadRegistry()).find(getRouterParam(event, 'identifier', { decode: true }) ?? '')
  if (!record) {
    throw createError({ statusCode: 404, statusMessage: 'Règle introuvable' })
  }
  return toRecordDetail(record)
})
