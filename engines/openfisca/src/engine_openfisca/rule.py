from dataclasses import dataclass

from engine_openfisca import periods
from engine_openfisca.system import load_system, variable


@dataclass(frozen=True)
class OpenfiscaRule:
    """A rule written with OpenFisca: the module of its system, the variables it computes and the variables it reads."""

    system: str
    outputs: tuple[str, ...]
    inputs: tuple[str, ...]


def read_rule(rule: OpenfiscaRule):
    """The variables and the unit of the period of a rule, checked against its system."""
    system = load_system(rule.system)
    outputs = [variable(system, name) for name in rule.outputs]
    inputs = [variable(system, name) for name in rule.inputs]
    unit = periods.rule_unit(outputs)
    for input_variable in inputs:
        periods.check_input(input_variable, unit)
    return system, outputs, inputs, unit
