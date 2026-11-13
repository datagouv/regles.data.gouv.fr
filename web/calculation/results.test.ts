import { expect, it } from 'vitest'
import { presentResults } from './results'

it('presents the outputs that the output schema names, in its order, formatted in French', () => {
  const outputSchema = {
    properties: {
      eligible: { title: 'Peut voter' },
      internal: {},
      amount: { title: 'Quotient familial' },
    },
  }

  expect(presentResults(outputSchema, { amount: 1666.67, internal: 3, eligible: true })).toEqual([
    { label: 'Peut voter', value: 'Oui' },
    { label: 'Quotient familial', value: '1\u202F666,67' },
  ])
})

it('leaves out a named output that the service did not return', () => {
  expect(presentResults({
    properties: {
      amount: { title: 'Montant' },
    },
  }, {})).toEqual([])
})
