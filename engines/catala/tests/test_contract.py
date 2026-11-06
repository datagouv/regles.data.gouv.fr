import pytest
from cases import EXECUTABLE, UNSUPPORTED
from jsonschema import Draft202012Validator, validate

from engine_catala import execute, infer_call_contract


@pytest.mark.parametrize("target", [*EXECUTABLE, *UNSUPPORTED])
def test_the_schemas_are_valid_json_schemas(target):
    contract = infer_call_contract(target)

    Draft202012Validator.check_schema(contract["input_schema"])
    Draft202012Validator.check_schema(contract["output_schema"])


@pytest.mark.parametrize("target", EXECUTABLE)
def test_the_sample_input_fits_the_input_schema(target):
    contract = infer_call_contract(target)

    assert contract["warnings"] == []
    validate(contract["sample_input"], contract["input_schema"])


@pytest.mark.parametrize(("target", "inputs"), [(target, inputs) for target, (inputs, _) in EXECUTABLE.items()])
def test_the_inputs_and_the_output_fit_the_schemas(target, inputs):
    contract = infer_call_contract(target)

    validate(inputs, contract["input_schema"])
    validate(execute(target, inputs), contract["output_schema"])


@pytest.mark.parametrize("target", UNSUPPORTED)
def test_an_enumeration_input_is_reported(target):
    assert infer_call_contract(target)["warnings"]
