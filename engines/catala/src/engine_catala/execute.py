from engine_catala.errors import ScopeError
from engine_catala.scope import load_scope
from engine_catala.values import from_catala, is_scope_error, runtime_of, to_catala


def execute(target: str, inputs: dict) -> dict:
    """Run the scope that `target` designates on JSON inputs and return its JSON output."""
    scope = load_scope(target)
    runtime = runtime_of(scope.module)
    catala_input = to_catala(inputs, scope.input_type, runtime)
    try:
        output = scope.function(catala_input)
    except Exception as error:
        if is_scope_error(error, runtime):
            raise ScopeError(str(error)) from error
        raise
    return from_catala(output, runtime)
