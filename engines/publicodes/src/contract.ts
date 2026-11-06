import type { PublicodesRule } from './rule.ts'
import type { JsonSchema } from './values.ts'
import { keyOf } from './keys.ts'
import { engineFor } from './rule.ts'
import { inputSchemaOf, outputSchemaOf, sampleOf } from './values.ts'

export interface CallContract {
  inputSchema: JsonSchema
  outputSchema: JsonSchema
  sampleInput: Record<string, unknown>
  warnings: string[]
}

/**
 * Infer the input and output JSON Schemas of a rule, with a sample input.
 * No input is required: the inputs that an output needs depend on the other answers.
 */
export function inferCallContract(rule: PublicodesRule): CallContract {
  const engine = engineFor(rule)
  const properties = Object.fromEntries(rule.inputs.map(name => [keyOf(name), inputSchemaOf(engine, name)]))
  const inputSchema = { type: 'object', properties, additionalProperties: false }
  const outputSchema = {
    type: 'object',
    required: rule.outputs.map(keyOf),
    properties: Object.fromEntries(rule.outputs.map(name => [keyOf(name), outputSchemaOf(engine, name)])),
    additionalProperties: false,
  }
  const sampleInput = Object.fromEntries(Object.entries(properties).map(([key, schema]) => [key, sampleOf(schema)]))
  return { inputSchema, outputSchema, sampleInput, warnings: [] }
}
