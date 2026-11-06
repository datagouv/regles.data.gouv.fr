from openfisca_core.errors import SituationParsingError
from openfisca_core.simulations import SimulationBuilder

from engine_openfisca import periods
from engine_openfisca.rule import OpenfiscaRule, read_rule
from engine_openfisca.values import to_json

PERSON = "person"
GROUP = "group"


def execute(rule: OpenfiscaRule, inputs: dict) -> dict:
    """Compute the outputs of a rule for one person, each group entity holding that person alone."""
    system, outputs, input_variables, unit = read_rule(rule)
    missing = [name for name in ("period", *rule.inputs) if name not in inputs]
    if missing:
        raise ValueError(f"the inputs miss {missing}")
    requested = periods.parse(str(inputs["period"]), unit)

    situation = {system.person_entity.plural: {PERSON: {}}}
    for entity in system.group_entities:
        first_role = entity.roles[0]
        situation[entity.plural] = {GROUP: {first_role.plural or first_role.key: [PERSON]}}
    for item in input_variables:
        member = PERSON if item.entity.is_person else GROUP
        situation[item.entity.plural][member][item.name] = {str(periods.input_period(item, requested, rule.rolling_year_inputs)): inputs[item.name]}

    try:
        simulation = SimulationBuilder().build_from_entities(system, situation)
    except SituationParsingError as error:
        raise ValueError(f"OpenFisca cannot read the inputs: {error.error}") from error
    return {item.name: to_json(simulation.calculate(item.name, requested), item) for item in outputs}
