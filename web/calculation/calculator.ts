import type { CallContract } from './service'
import { CalculationError, executeRule, fetchCallContract } from './service'

/** What the input form of a rule calls: a calculation service, or an engine that runs in the page. */
export interface Calculator {
  callContract: () => Promise<CallContract>
  execute: (inputs: Record<string, unknown>) => Promise<Record<string, unknown>>
}

export function serviceCalculator(service: string, rule: string, fetcher: typeof fetch = fetch): Calculator {
  return {
    callContract: () => fetchCallContract(service, rule, fetcher),
    execute: inputs => executeRule(service, rule, inputs, fetcher),
  }
}

/**
 * A calculator that runs a rule in the page. An error named InputError, as engine adapters
 * name an input outside the schema, is refused; any other error is a failed calculation.
 */
export function localCalculator(contract: CallContract, run: (inputs: Record<string, unknown>) => Record<string, unknown>): Calculator {
  return {
    callContract: async () => contract,
    execute: async (inputs) => {
      try {
        return run(inputs)
      }
      catch (error) {
        const message = error instanceof Error
          ? error.message
          : String(error)
        throw new CalculationError(error instanceof Error && error.name === 'InputError'
          ? 'refused'
          : 'failed', message)
      }
    },
  }
}
