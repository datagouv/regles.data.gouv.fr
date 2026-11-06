import pytest
from cases import AGE, EXECUTIONS, PASS_CULTURE, PRIME_ACTIVITE, UNREADABLE
from jsonschema import validate
from openfisca_core.simulations import SimulationBuilder

from engine_openfisca import execute, infer_call_contract
from engine_openfisca.system import load_system


@pytest.mark.parametrize(("rule", "inputs", "expected"), EXECUTIONS, ids=lambda value: str(value)[:40])
def test_a_rule_gives_the_expected_output_valid_against_its_schema(rule, inputs, expected):
    output = execute(rule, inputs)

    assert output == expected
    validate(output, infer_call_contract(rule)["output_schema"])


@pytest.mark.parametrize(("rule", "inputs"), UNREADABLE, ids=lambda value: str(value)[:40])
def test_an_unreadable_input_names_its_variable(rule, inputs):
    unreadable = next(name for name in rule.inputs if name in inputs)

    with pytest.raises(ValueError, match=unreadable):
        execute(rule, inputs)


def test_a_period_of_another_unit_is_refused():
    with pytest.raises(ValueError, match="is not one month"):
        execute(PASS_CULTURE, {"period": "2025", "date_naissance": "2007-02-01"})


def test_a_missing_input_is_named():
    with pytest.raises(ValueError, match="birth"):
        execute(AGE, {"period": "2025-04"})


def test_a_total_over_the_rolling_year_is_divided_among_its_months():
    system = load_system("openfisca_france")
    months = {f"{year}-{month:02d}": 1000 for year, month in [(2024, m) for m in range(3, 13)] + [(2025, 1), (2025, 2)]}
    situation = {"individus": {"p": {"salaire_imposable": months}}}
    for entity in system.group_entities:
        role = entity.roles[0]
        situation[entity.plural] = {"g": {role.plural or role.key: ["p"]}}
    by_month = SimulationBuilder().build_from_entities(system, situation).calculate("ppa", "2025-03")

    assert execute(PRIME_ACTIVITE, {"period": "2025-03", "salaire_imposable": 12000}) == {"ppa": float(str(by_month[0]))}
