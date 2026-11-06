export type JsonSchemaObject = Record<string, unknown> & { properties?: Record<string, JsonSchemaObject>, title?: string }

export interface CallContract {
  inputSchema: JsonSchemaObject
  outputSchema?: JsonSchemaObject
}

export async function fetchCallContract(service: string, rule: string, fetcher: typeof fetch = fetch): Promise<CallContract> {
  const response = await fetcher(`${service}/public/catalog/${encodeURIComponent(rule)}`)
  if (!response.ok) {
    throw new Error(String(response.status))
  }
  const body = await response.json() as { input_schema?: JsonSchemaObject, output_schema?: JsonSchemaObject }
  if (!body.input_schema) {
    throw new Error('missing input_schema')
  }
  return { inputSchema: body.input_schema, outputSchema: body.output_schema }
}

// refused: the service refused the inputs; failed: the rule computed no result for them; unavailable: any other answer
export type CalculationErrorKind = 'refused' | 'failed' | 'unavailable'

export class CalculationError extends Error {
  constructor(readonly kind: CalculationErrorKind, message: string) {
    super(message)
  }
}

export async function executeRule(service: string, rule: string, inputs: unknown, fetcher: typeof fetch = fetch): Promise<Record<string, unknown>> {
  const response = await fetcher(`${service}/public/execute/${encodeURIComponent(rule)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(inputs),
  })
  const result = await response.json().catch(() => ({})) as { status?: string, output?: Record<string, unknown>, error?: string, detail?: string }
  if (response.status >= 400 && response.status < 500) {
    throw new CalculationError('refused', result.detail ?? String(response.status))
  }
  if (!response.ok) {
    throw new CalculationError('unavailable', String(response.status))
  }
  if (result.status !== 'success' || !result.output) {
    throw new CalculationError('failed', result.error ?? String(result.status))
  }
  return result.output
}
