import { expect, it, vi } from 'vitest'
import { localCalculator, serviceCalculator } from './calculator'
import { CalculationError } from './service'

const CONTRACT = { inputSchema: { type: 'object' }, outputSchema: { type: 'object' } }

it('calls the calculation service for the contract and the execution', async () => {
  const fetcher = vi.fn<typeof fetch>(async () => new Response(JSON.stringify({ input_schema: {}, status: 'success', output: { a: 1 } })))
  const calculator = serviceCalculator('https://calcul.example', 'rule', fetcher)

  await calculator.callContract()
  expect(await calculator.execute({ x: 1 })).toEqual({ a: 1 })
  expect(fetcher.mock.calls.map(([address]) => address)).toEqual([
    'https://calcul.example/public/catalog/rule',
    'https://calcul.example/public/execute/rule',
  ])
})

it('runs a rule in the page with the contract it was given', async () => {
  const calculator = localCalculator(CONTRACT, inputs => ({ double: (inputs.x as number) * 2 }))

  expect(await calculator.callContract()).toBe(CONTRACT)
  expect(await calculator.execute({ x: 2 })).toEqual({ double: 4 })
})

it.each([
  ['InputError', 'refused'],
  ['Error', 'failed'],
])('classifies an error named %s as %s', async (name, kind) => {
  const calculator = localCalculator(CONTRACT, () => {
    throw Object.assign(new Error('no'), { name })
  })

  const error = await calculator.execute({}).catch(error => error)

  expect(error).toBeInstanceOf(CalculationError)
  expect(error).toMatchObject({ kind, message: 'no' })
})
