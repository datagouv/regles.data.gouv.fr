import type Engine from 'publicodes'

export type JsonSchema = Record<string, unknown>

// Publicodes reads a text between single quotes, and an empty text as a missing answer
const TEXT = { type: 'string', pattern: '^[^\']+$' }

/** The JSON Schema of an input, from the type, the possibilities and the default that the model gives it. */
export function inputSchemaOf(engine: Engine, dottedName: string): JsonSchema {
  const rule = engine.getRule(dottedName)
  const type = nodeType(engine, dottedName)
  if (!type) {
    throw new Error(`the model gives no type to the input '${dottedName}'`)
  }
  const schema: JsonSchema = { ...typeOf(engine, dottedName, type), title: rule.title }
  if (typeof rule.rawNode.description === 'string') {
    schema.description = rule.rawNode.description
  }
  const fallback = engine.evaluate(dottedName).nodeValue
  if (fallback !== undefined && fallback !== null) {
    schema.default = toJson(fallback, schema)
  }
  return schema
}

/** The JSON Schema of an output, null standing for a rule that does not apply. */
export function outputSchemaOf(engine: Engine, dottedName: string): JsonSchema {
  const type = nodeType(engine, dottedName)
  const json = type === 'date'
    ? { type: ['string', 'null'], format: 'date' }
    : { type: [type === 'number' || type === 'boolean'
        ? type
        : 'string', 'null'] }
  return { ...json, title: engine.getRule(dottedName).title }
}

/** A value that satisfies the schema of an input: its default, its first possibility, or a value of its type. */
export function sampleOf(schema: JsonSchema): unknown {
  if ('default' in schema) {
    return schema.default
  }
  if (Array.isArray(schema.oneOf)) {
    return (schema.oneOf[0] as { const: unknown }).const
  }
  if (schema.format === 'date') {
    return '2026-01-01'
  }
  return { number: 0, boolean: false, string: 'exemple' }[schema.type as string]
}

function typeOf(engine: Engine, dottedName: string, type: string): JsonSchema {
  const possibilities = engine.getPossibilitiesFor(dottedName)
  if (possibilities) {
    return {
      type: type === 'number'
        ? 'number'
        : 'string',
      oneOf: possibilities.map(possibility => ({
        const: possibility.nodeValue,
        title: possibility.type === 'reference' && possibility.dottedName
          ? engine.getRule(possibility.dottedName).title
          : String(possibility.nodeValue),
      })),
    }
  }
  switch (type) {
    case 'number':
    case 'boolean':
      return { type }
    case 'date':
      return { type: 'string', format: 'date' }
    default:
      return TEXT
  }
}

function nodeType(engine: Engine, dottedName: string): string | undefined {
  return engine.context.nodesTypes.get(engine.getRule(dottedName))?.type
}

/** The value of an output in JSON: a date in ISO 8601, null for a rule that does not apply. */
export function toJson(value: unknown, schema: JsonSchema): unknown {
  if (typeof value === 'string' && schema.format === 'date') {
    return value.split('/').reverse().join('-')
  }
  return value
}
