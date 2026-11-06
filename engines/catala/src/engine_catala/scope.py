import importlib
import inspect
import typing
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Callable


@dataclass(frozen=True)
class Scope:
    module: ModuleType
    function: Callable[[Any], Any]
    input_type: type
    output_type: type | None


def load_scope(target: str) -> Scope:
    """Load the scope that `target`, written `module:function`, designates in a module compiled by Catala."""
    module_name, separator, function_name = target.partition(":")
    if not separator or not module_name or not function_name:
        raise ValueError(f"the target {target!r} is not written module:function")
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)
    parameters = list(inspect.signature(function).parameters)
    if len(parameters) != 1:
        raise ValueError(f"the scope {target!r} does not take exactly one input structure")
    # compiled modules use `from __future__ import annotations`: get_type_hints resolves the annotations
    hints = typing.get_type_hints(function)
    input_type = hints.get(parameters[0])
    if input_type is None:
        raise ValueError(f"the input of the scope {target!r} has no type annotation")
    return Scope(module, function, input_type, hints.get("return"))
