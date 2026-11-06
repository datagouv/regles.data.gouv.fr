from dataclasses import dataclass

from engine_openfisca import periods
from engine_openfisca.system import load_system, variable


@dataclass(frozen=True)
class OpenfiscaRule:
    """A rule written with OpenFisca: the module of its system, the variables it computes, the variables it reads and those of them read over the rolling year."""

    system: str
    outputs: tuple[str, ...]
    inputs: tuple[str, ...]
    rolling_year_inputs: tuple[str, ...] = ()


def read_rule(rule: OpenfiscaRule):
    """The variables and the unit of the period of a rule, checked against its system."""
    system = load_system(rule.system)
    outputs = [variable(system, name) for name in rule.outputs]
    inputs = [variable(system, name) for name in rule.inputs]
    unit = periods.rule_unit(outputs)
    for input_variable in inputs:
        periods.check_input(input_variable, unit)
    for name in rule.rolling_year_inputs:
        periods.check_rolling_year_input(variable(system, name), rule.inputs)
    return system, outputs, inputs, unit
