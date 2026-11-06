import Engine from 'publicodes'

export interface PublicodesRule {
  /** The compiled rules of a Publicodes model, as `publicodes compile` writes them. */
  model: Record<string, unknown>
  /** The dotted names of the rules that the rule computes. */
  outputs: string[]
  /** The dotted names of the rules that the rule reads from its inputs. */
  inputs: string[]
}

const OPTIONS = {
  logger: { log: () => {}, warn: () => {}, error: () => {} },
}

const engines = new WeakMap<object, Engine>()

/** An engine with an empty situation, copied from an engine parsed once per model. */
export function engineFor(rule: PublicodesRule): Engine {
  let engine = engines.get(rule.model)
  if (!engine) {
    engine = new Engine(rule.model as ConstructorParameters<typeof Engine>[0], OPTIONS)
    engines.set(rule.model, engine)
  }
  checkNames(rule, engine)
  return engine.shallowCopy()
}

function checkNames(rule: PublicodesRule, engine: Engine): void {
  for (const name of [...rule.outputs, ...rule.inputs]) {
    if (!(name in engine.getParsedRules())) {
      throw new Error(`the model has no rule '${name}'`)
    }
    if (name.includes('__')) {
      throw new Error(`the rule '${name}' has a name that holds '__', which encodes the separator of its key`)
    }
  }
}
