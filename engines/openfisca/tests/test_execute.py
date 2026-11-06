import pytest
from cases import AGE, EXECUTIONS, PASS_CULTURE, UNREADABLE
from jsonschema import validate

from engine_openfisca import execute, infer_call_contract


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
