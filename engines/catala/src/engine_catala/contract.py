from engine_catala.scope import load_scope
from engine_catala.values import runtime_of, sample_of, schema_of


def infer_call_contract(target: str) -> dict:
    """Infer the input and output JSON Schemas of the scope that `target` designates, with a sample input."""
    scope = load_scope(target)
    runtime = runtime_of(scope.module)
    warnings: list[str] = []
    input_schema = schema_of(scope.input_type, runtime, "input", warnings)
    output_schema = schema_of(scope.output_type, runtime, "output", warnings)
    return {
        "input_schema": input_schema,
        "output_schema": output_schema,
        "sample_input": sample_of(scope.input_type, runtime),
        "warnings": warnings,
    }
