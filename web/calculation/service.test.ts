import { describe, expect, it, vi } from 'vitest'
import { CalculationError, executeRule, fetchCallContract } from './service'

const SERVICE = 'https://calcul.example'

function answering(status: number, body: unknown) {
  return vi.fn<typeof fetch>(async () => new Response(JSON.stringify(body), { status }))
}

describe('fetchCallContract', () => {
  it('reads the schemas of the rule, with its identifier encoded in the address', async () => {
    const fetcher = answering(200, { input_schema: { type: 'object' }, output_schema: { type: 'object' } })

    const contract = await fetchCallContract(SERVICE, 'a/b c', fetcher)

    expect(fetcher).toHaveBeenCalledWith(`${SERVICE}/public/catalog/a%2Fb%20c`)
    expect(contract).toEqual({ inputSchema: { type: 'object' }, outputSchema: { type: 'object' } })
  })

  it('fails when the service answers with an error status', async () => {
    await expect(fetchCallContract(SERVICE, 'rule', answering(404, {}))).rejects.toThrow('404')
  })

  it('fails when the answer has no input schema', async () => {
    await expect(fetchCallContract(SERVICE, 'rule', answering(200, { output_schema: {} }))).rejects.toThrow('input_schema')
  })
})

describe('executeRule', () => {
  it('posts the inputs and returns the output', async () => {
    const fetcher = answering(200, { status: 'success', output: { quotient_familial: 666.67 } })

    const output = await executeRule(SERVICE, 'a/b', { menage: {} }, fetcher)

    expect(fetcher).toHaveBeenCalledWith(`${SERVICE}/public/execute/a%2Fb`, expect.objectContaining({ method: 'POST', body: '{"menage":{}}' }))
    expect(output).toEqual({ quotient_familial: 666.67 })
  })

  it.each([
    [400, { detail: 'input validation error' }, 'refused', 'input validation error'],
    [500, {}, 'unavailable', '500'],
    [200, { status: 'failed', error: 'division by zero' }, 'failed', 'division by zero'],
  ])('classifies an answer %i as an error of kind %s', async (status, body, kind, message) => {
    const error = await executeRule(SERVICE, 'rule', {}, answering(status as number, body)).catch(error => error)

    expect(error).toBeInstanceOf(CalculationError)
    expect(error).toMatchObject({ kind, message })
  })
})
