import pytest
from cases import EXECUTABLE, MODULES, UNSUPPORTED

from engine_catala import ScopeError, UnsupportedType, execute

QUOTIENT_FAMILIAL = f"{MODULES}.Quotient_familial:calcul_quotient_familial"


@pytest.mark.parametrize(("target", "inputs", "expected"), [(target, *case) for target, case in EXECUTABLE.items()])
def test_a_scope_gives_the_recorded_output(target, inputs, expected):
    assert execute(target, inputs) == expected


def test_the_family_quotient_of_prestagri_is_computed():
    inputs, _ = EXECUTABLE[QUOTIENT_FAMILIAL]

    assert execute(QUOTIENT_FAMILIAL, inputs)["quotient_familial"] == 666.67


def test_a_computation_that_the_scope_refuses_raises_a_scope_error():
    inputs, _ = EXECUTABLE[QUOTIENT_FAMILIAL]
    household = {**inputs["menage"], "parent_isole": False, "membres_du_foyer": []}

    with pytest.raises(ScopeError, match="division by zero"):
        execute(QUOTIENT_FAMILIAL, {"menage": household})


def test_a_missing_input_field_is_named():
    with pytest.raises(ValueError, match="menage"):
        execute(QUOTIENT_FAMILIAL, {})


@pytest.mark.parametrize("target", UNSUPPORTED)
def test_an_enumeration_input_is_unsupported(target):
    with pytest.raises(UnsupportedType):
        execute(target, {"criteres": [{"code": "C1", "payload": None}]})


def test_a_target_that_is_not_module_and_function_is_refused():
    with pytest.raises(ValueError, match="module:function"):
        execute("prestagri.generated.Quotient_familial", {})
