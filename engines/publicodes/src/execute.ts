import type { ValidateFunction } from 'ajv/dist/2020.js'
import type { PublicodesRule } from './rule.ts'
import type { JsonSchema } from './values.ts'
import ajvFormats from 'ajv-formats'
import { Ajv2020 } from 'ajv/dist/2020.js'
import { inferCallContract } from './contract.ts'
import { dottedNameOf, keyOf } from './keys.ts'
import { engineFor } from './rule.ts'
import { toJson, toSituationValue } from './values.ts'

/** An input outside the input schema of a rule, or an answer missing to compute an output. */
export class InputError extends Error {
  override name = 'InputError'
}

const ajv = new Ajv2020({ allErrors: true })
ajvFormats.default(ajv)

interface CompiledRule {
  validate: ValidateFunction
  outputs: Record<string, JsonSchema>
}

// ajv keeps each schema it compiles: one compilation per rule
const compiled = new WeakMap<PublicodesRule, CompiledRule>()

function compile(rule: PublicodesRule): CompiledRule {
  let entry = compiled.get(rule)
  if (!entry) {
    const { inputSchema, outputSchema } = inferCallContract(rule)
    entry = { validate: ajv.compile(inputSchema), outputs: outputSchema.properties as Record<string, JsonSchema> }
    compiled.set(rule, entry)
  }
  return entry
}

/** Compute the outputs of a rule from JSON inputs, keyed as its input schema names them. */
export function execute(rule: PublicodesRule, inputs: Record<string, unknown>): Record<string, unknown> {
  const { validate, outputs } = compile(rule)
  // Publicodes reads a string of a situation as an expression: an input is checked before it reaches the engine
  if (!validate(inputs)) {
    throw new InputError(ajv.errorsText(validate.errors, { dataVar: 'inputs' }))
  }
  const engine = engineFor(rule)
  engine.setSituation(Object.fromEntries(Object.entries(inputs).map(([key, value]) => {
    const name = dottedNameOf(key)
    return [name, toSituationValue(engine, name, value)]
  })))
  return Object.fromEntries(rule.outputs.map((name) => {
    const evaluation = engine.evaluate(name)
    if (evaluation.nodeValue === undefined) {
      const missing = Object.keys(evaluation.missingVariables)
      const message = `the output '${name}' misses ${missing.map(variable => `'${variable}'`).join(', ')}`
      throw missing.every(variable => rule.inputs.includes(variable))
        ? new InputError(message)
        : new Error(message)
    }
    return [keyOf(name), toJson(evaluation.nodeValue, outputs[keyOf(name)]!)]
  }))
}
