import pytest
from cases import PASS_CULTURE, PRIME_ACTIVITE, REFUSED, RULES
from jsonschema import Draft202012Validator, ValidationError, validate

from engine_openfisca import infer_call_contract


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule.outputs[0])
def test_the_contract_is_valid_json_schema_with_a_valid_sample(rule):
    contract = infer_call_contract(rule)

    Draft202012Validator.check_schema(contract["input_schema"])
    Draft202012Validator.check_schema(contract["output_schema"])
    validate(contract["sample_input"], contract["input_schema"])


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule.outputs[0])
def test_the_period_and_every_input_are_required(rule):
    assert infer_call_contract(rule)["input_schema"]["required"] == ["period", *rule.inputs]


def test_the_contract_of_the_pass_culture_comes_from_openfisca_france():
    contract = infer_call_contract(PASS_CULTURE)

    assert contract["input_schema"]["properties"]["date_naissance"] == {"type": "string", "format": "date", "title": "Date de naissance"}
    assert contract["output_schema"]["properties"]["pass_culture"] == {"type": "number", "title": "Montant du pass culture"}


@pytest.mark.parametrize("period", ["2025-13", "2025", "2025-04-01"])
def test_the_period_of_a_monthly_rule_is_a_month(period):
    with pytest.raises(ValidationError):
        validate({"period": period, "date_naissance": "2007-02-01"}, infer_call_contract(PASS_CULTURE)["input_schema"])


@pytest.mark.parametrize(("rule", "reason"), REFUSED.values(), ids=REFUSED.keys())
def test_a_rule_that_the_engine_cannot_read_is_refused(rule, reason):
    with pytest.raises(ValueError, match=reason):
        infer_call_contract(rule)


def test_an_input_read_over_the_rolling_year_says_so():
    salary = infer_call_contract(PRIME_ACTIVITE)["input_schema"]["properties"]["salaire_imposable"]

    assert salary["description"] == "Total des douze mois qui précèdent le mois du calcul."
