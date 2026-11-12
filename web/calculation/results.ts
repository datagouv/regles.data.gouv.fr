import type { JsonSchemaObject } from './service'

export interface CalculationResult {
  label: string
  value: string
}

export function presentResults(outputSchema: JsonSchemaObject | undefined, output: Record<string, unknown>): CalculationResult[] {
  return Object.entries(outputSchema?.properties ?? {})
    .filter(([name, schema]) => schema.title && output[name] !== undefined)
    .map(([name, schema]) => ({ label: schema.title!, value: format(output[name]) }))
}

function format(value: unknown): string {
  if (typeof value === 'boolean') {
    return value
      ? 'Oui'
      : 'Non'
  }
  if (typeof value === 'number') {
    return value.toLocaleString('fr-FR')
  }
  return String(value)
}
