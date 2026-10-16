import { toCataloguePage } from '../../../catalogue/record'

export default defineEventHandler(async () => {
  return toCataloguePage((await loadRegistry()).records)
})
