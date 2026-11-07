import ajvFormats from 'ajv-formats'
import { Ajv2020 } from 'ajv/dist/2020.js'
import { expect, it } from 'vitest'
import { execute, inferCallContract, InputError } from '../src/index.ts'
import { CIR_AMOUNT, EXECUTIONS, TYPES, TYPES_MODEL } from './cases.ts'

const ajv = new Ajv2020()
ajvFormats.default(ajv)

it.each(EXECUTIONS)('computes %s, valid against the output schema', (_, rule, inputs, expected) => {
  const output = execute(rule, inputs)

  expect(output).toEqual(expected)
  expect(ajv.validate(inferCallContract(rule).outputSchema, output)).toBe(true)
})

it('writes a date in ISO 8601, and null for a rule that does not apply', () => {
  expect(execute(TYPES, { début: '2025-06-30', taux: 5 })).toEqual({ fin: '2025-06-30', bonus: null })
  expect(execute(TYPES, { taux: 10, salarié: true })).toEqual({ fin: '2024-02-01', bonus: 10 })
})

it('starts each call from an empty situation', () => {
  execute(CIR_AMOUNT, { cir__depensesMetropole: 100000, cir__depensesDom: 0 })

  expect(execute(CIR_AMOUNT, {})).toEqual({ cir__montant: 0 })
})

it.each([
  ['a text given to a number, which Publicodes would read as a rule', { cir__depensesMetropole: 'secret' }, 'must be number'],
  ['an unknown key', { cir__inconnu: 1 }, 'must NOT have additional properties'],
])('refuses %s before the engine reads it', (_, inputs, reason) => {
  expect(() => execute(CIR_AMOUNT, inputs)).toThrow(InputError)
  expect(() => execute(CIR_AMOUNT, inputs)).toThrow(reason)
})

it.each([
  ['an invalid date', { début: '2024-02-30', taux: 5 }],
  ['an empty text, which Publicodes reads as a missing answer', { nom: '', taux: 5 }],
  ['a text that holds a quote, which would close the text that Publicodes reads', { nom: 'x\' + 1 + \'', taux: 5 }],
])('refuses %s', (_, inputs) => {
  expect(() => execute(TYPES, inputs)).toThrow(InputError)
})

it('refuses the inputs that miss an answer an output needs, with its name', () => {
  expect(() => execute(TYPES, { salarié: true })).toThrow(InputError)
  expect(() => execute(TYPES, { salarié: true })).toThrow('\'taux\'')
})

it('names the variables that an output misses outside its inputs', () => {
  const rule = { model: TYPES_MODEL, outputs: ['reste'], inputs: [] }

  expect(() => execute(rule, {})).toThrow('\'inconnu\'')
  expect(() => execute(rule, {})).not.toThrow(InputError)
})
