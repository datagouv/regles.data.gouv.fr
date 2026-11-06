from openfisca_core.periods import DateUnit, Period, period as parse_period
from openfisca_core.variables import Variable

PATTERNS = {DateUnit.MONTH: r"^\d{4}-(0[1-9]|1[0-2])$", DateUnit.YEAR: r"^\d{4}$"}
SAMPLES = {DateUnit.MONTH: "2026-01", DateUnit.YEAR: "2026"}
DESCRIPTIONS = {
    DateUnit.MONTH: "Mois du calcul, au format AAAA-MM, par exemple 2026-01.",
    DateUnit.YEAR: "Année du calcul, au format AAAA, par exemple 2026.",
}


def rule_unit(outputs: list[Variable]) -> DateUnit:
    """The unit of the period of a rule: the definition period shared by its outputs, a month or a year."""
    units = {output.definition_period for output in outputs}
    if len(units) != 1 or next(iter(units)) not in PATTERNS:
        raise ValueError(f"the outputs of a rule share one definition period, a month or a year, not {sorted(map(str, units))}")
    return next(iter(units))


def check_input(variable: Variable, unit: DateUnit) -> None:
    if variable.definition_period not in (DateUnit.ETERNITY, unit, DateUnit.YEAR):
        raise ValueError(f"the input {variable.name} is defined by {variable.definition_period}, which a rule by {unit} cannot read")


def input_period(variable: Variable, requested: Period) -> Period:
    """The period at which an input is set: the requested one, or its year for a yearly input of a monthly rule."""
    if variable.definition_period == DateUnit.YEAR:
        return requested.this_year
    return requested


def parse(text: str, unit: DateUnit) -> Period:
    requested = parse_period(text)
    if requested.unit != unit or requested.size != 1:
        raise ValueError(f"the period {text!r} is not one {unit}")
    return requested
