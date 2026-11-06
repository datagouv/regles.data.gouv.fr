import ajvFormats from 'ajv-formats'
import { Ajv2020 } from 'ajv/dist/2020.js'
import { describe, expect, it } from 'vitest'
import { inferCallContract } from '../src/index.ts'
import { CIR_AMOUNT, CIR_ELIGIBILITY, TYPES, TYPES_MODEL } from './cases.ts'

const ajv = new Ajv2020()
ajvFormats.default(ajv)

describe.each([CIR_AMOUNT, CIR_ELIGIBILITY, TYPES])('the contract of $outputs', (rule) => {
  const contract = inferCallContract(rule)

  it('is valid JSON Schema, with a valid sample input', () => {
    expect(ajv.validateSchema(contract.inputSchema)).toBe(true)
    expect(ajv.validateSchema(contract.outputSchema)).toBe(true)
    expect(ajv.validate(contract.inputSchema, contract.sampleInput), JSON.stringify(ajv.errors)).toBe(true)
  })
})

it('reads the possibilities of a rule, with no input required', () => {
  const { inputSchema } = inferCallContract(CIR_ELIGIBILITY)

  expect(inputSchema).not.toHaveProperty('required')
  expect((inputSchema.properties as Record<string, any>).regimeFiscal.oneOf).toEqual([
    { const: 'micro', title: 'micro' },
    { const: 'reel-simplifie', title: 'reel-simplifie' },
    { const: 'reel-normal', title: 'reel-normal' },
  ])
})

it('names the inputs by their encoded keys, with their default', () => {
  const { inputSchema } = inferCallContract(CIR_AMOUNT)

  expect(inputSchema.properties).toMatchObject({ cir__depensesMetropole: { type: 'number', default: 0 } })
})

it('writes the types and the defaults of Publicodes in JSON', () => {
  const { inputSchema, outputSchema } = inferCallContract(TYPES)

  expect(inputSchema.properties).toMatchObject({
    début: { type: 'string', format: 'date', default: '2024-02-01' },
    nom: { type: 'string', description: 'Nom d\'usage', default: 'x' },
    motif: { type: 'string', pattern: '^[^\']+$' },
    salarié: { type: 'boolean', default: false },
    taux: { type: 'number', oneOf: [{ const: 5 }, { const: 10 }] },
    prime: { type: 'number' },
    contrat: { type: 'string', oneOf: [{ const: 'CDI', title: 'Contrat à durée indéterminée' }, { const: 'CDD', title: 'Contrat à durée déterminée' }] },
  })
  expect((inputSchema.properties as Record<string, object>).prime).not.toHaveProperty('default')
  expect(outputSchema.properties).toMatchObject({
    fin: { type: ['string', 'null'], format: 'date' },
    bonus: { type: ['number', 'null'] },
  })
})

it.each([
  ['an unknown rule', ['absente'], 'no rule \'absente\''],
  ['a name that holds the separator of a key', ['a__b'], 'holds \'__\''],
  ['an input with no type', ['sansType'], 'no type to the input \'sansType\''],
])('refuses %s', (_, inputs, reason) => {
  const model = { ...TYPES_MODEL, a__b: { type: 'nombre' }, sansType: {} }

  expect(() => inferCallContract({ model, outputs: ['fin'], inputs })).toThrow(reason)
})
