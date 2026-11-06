import importlib

from engine_catala.values import from_catala, runtime_of, schema_of, to_catala

RUNTIME = runtime_of(importlib.import_module("prestagri.generated.Quotient_familial"))


def test_a_date_goes_to_catala_and_back():
    date_type = RUNTIME.get("Date")

    assert from_catala(to_catala("2026-03-31", date_type, RUNTIME), RUNTIME) == "2026-03-31"
    assert schema_of(date_type, RUNTIME, "input", []) == {"type": "string", "format": "date"}
