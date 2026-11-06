from openfisca_core.holders import set_input_divide_by_period
from openfisca_core.periods import DateUnit, Period, period as parse_period
from openfisca_core.variables import Variable

PATTERNS = {DateUnit.MONTH: r"^\d{4}-(0[1-9]|1[0-2])$", DateUnit.YEAR: r"^\d{4}$"}
SAMPLES = {DateUnit.MONTH: "2026-01", DateUnit.YEAR: "2026"}
DESCRIPTIONS = {
    DateUnit.MONTH: "Mois du calcul, au format AAAA-MM, par exemple 2026-01.",
    DateUnit.YEAR: "Année du calcul, au format AAAA, par exemple 2026.",
}
ROLLING_YEAR_DESCRIPTION = "Total des douze mois qui précèdent le mois du calcul."


def rule_unit(outputs: list[Variable]) -> DateUnit:
    """The unit of the period of a rule: the definition period shared by its outputs, a month or a year."""
    units = {output.definition_period for output in outputs}
    if len(units) != 1 or next(iter(units)) not in PATTERNS:
        raise ValueError(f"the outputs of a rule share one definition period, a month or a year, not {sorted(map(str, units))}")
    return next(iter(units))


def check_input(variable: Variable, unit: DateUnit) -> None:
    if variable.definition_period not in (DateUnit.ETERNITY, unit, DateUnit.YEAR):
        raise ValueError(f"the input {variable.name} is defined by {variable.definition_period}, which a rule by {unit} cannot read")


def check_rolling_year_input(variable: Variable, inputs: tuple[str, ...]) -> None:
    """Refuse an input that cannot be read over the rolling year; check_input already refuses a monthly input of a yearly rule."""
    if variable.name not in inputs:
        raise ValueError(f"the rolling year input {variable.name} is not an input of the rule")
    if variable.definition_period != DateUnit.MONTH:
        raise ValueError(f"the rolling year input {variable.name} is not defined by month")
    # a variable that dispatches its input would copy the total on each month
    if variable.set_input is not set_input_divide_by_period:
        raise ValueError(f"the rolling year input {variable.name} does not divide its input among the months")


def rolling_year(requested: Period) -> Period:
    """The twelve months before the requested month."""
    return Period((DateUnit.MONTH, requested.offset(-12).start, 12))


def input_period(variable: Variable, requested: Period, rolling_year_inputs: tuple[str, ...]) -> Period:
    """The period at which an input is set: the requested one, the rolling year, or its year for a yearly input of a monthly rule."""
    if variable.name in rolling_year_inputs:
        return rolling_year(requested)
    if variable.definition_period == DateUnit.YEAR:
        return requested.this_year
    return requested


def parse(text: str, unit: DateUnit) -> Period:
    requested = parse_period(text)
    if requested.unit != unit or requested.size != 1:
        raise ValueError(f"the period {text!r} is not one {unit}")
    return requested
