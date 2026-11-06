import typing
from dataclasses import dataclass
from types import ModuleType
from typing import Any

from engine_catala.errors import UnsupportedType

RUNTIME_CLASSES = ("Money", "Integer", "Decimal", "Bool", "Date", "Option", "Array", "CatalaStruct", "CatalaEnum", "CatalaError")


@dataclass(frozen=True)
class Runtime:
    """The classes of the runtime that a compiled module imports, read in its namespace."""

    classes: dict[str, type]

    def get(self, name: str) -> type | None:
        return self.classes.get(name)

    def is_instance(self, value: Any, name: str) -> bool:
        cls = self.get(name)
        return cls is not None and isinstance(value, cls)

    def is_subclass(self, value_type: Any, name: str) -> bool:
        cls = self.get(name)
        return cls is not None and isinstance(value_type, type) and issubclass(value_type, cls)


def runtime_of(module: ModuleType) -> Runtime:
    return Runtime({name: getattr(module, name) for name in RUNTIME_CLASSES if hasattr(module, name)})


def is_scope_error(error: BaseException, runtime: Runtime) -> bool:
    return runtime.is_instance(error, "CatalaError")


def input_key(field: str) -> str:
    """The JSON key of a field of an input structure: Catala suffixes the fields of a scope input with `_in`."""
    return field.removesuffix("_in")


def struct_fields(struct_type: type) -> dict[str, Any]:
    hints = typing.get_type_hints(struct_type)
    return {field: hints[field] for field in struct_type.fields}


def _container(value_type: Any, runtime: Runtime) -> str | None:
    origin = typing.get_origin(value_type)
    if origin is None:
        return None
    if origin is runtime.get("Option"):
        return "Option"
    # compiled structures annotate lists with typing.List, the runtime builds Array values
    if origin in (runtime.get("Array"), list):
        return "Array"
    return None


def to_catala(value: Any, value_type: Any, runtime: Runtime) -> Any:
    container = _container(value_type, runtime)
    (item_type, *_) = typing.get_args(value_type) or (None,)
    if container == "Option":
        return runtime.get("Option")(None if value is None else to_catala(value, item_type, runtime))
    if container == "Array":
        if not isinstance(value, list):
            raise ValueError(f"expected a list, got {type(value).__name__}")
        return runtime.get("Array")([to_catala(item, item_type, runtime) for item in value])

    if runtime.is_subclass(value_type, "CatalaStruct"):
        if not isinstance(value, dict):
            raise ValueError(f"expected an object for the structure {value_type.__name__}, got {type(value).__name__}")
        fields = struct_fields(value_type)
        missing = sorted(input_key(field) for field in fields if input_key(field) not in value)
        if missing:
            raise ValueError(f"missing fields {missing} for the structure {value_type.__name__}")
        return value_type(**{field: to_catala(value[input_key(field)], field_type, runtime) for field, field_type in fields.items()})

    if value_type is runtime.get("Money") or value_type is runtime.get("Decimal"):
        # built from a string to avoid the rounding of binary floats
        return value_type(str(value))
    if value_type is runtime.get("Integer"):
        return value_type(int(value))
    if value_type is runtime.get("Bool"):
        return value_type(bool(value))
    if value_type is runtime.get("Date"):
        year, month, day = str(value).split("-")
        return value_type((int(year), int(month), int(day)))

    raise UnsupportedType(f"no conversion from JSON to the Catala type {getattr(value_type, '__name__', value_type)}")


def from_catala(value: Any, runtime: Runtime) -> Any:
    if runtime.is_instance(value, "Option"):
        return None if value.value is None else from_catala(value.value, runtime)
    if runtime.is_instance(value, "Array"):
        return [from_catala(item, runtime) for item in value]
    if runtime.is_instance(value, "CatalaStruct"):
        return {field: from_catala(getattr(value, field), runtime) for field in value.fields}
    if runtime.is_instance(value, "CatalaEnum"):
        return {"code": value.code.name, "payload": from_catala(value.payload, runtime)}
    if runtime.is_instance(value, "Money") or runtime.is_instance(value, "Decimal"):
        return float(value)
    if runtime.is_instance(value, "Integer"):
        return int(value)
    if runtime.is_instance(value, "Bool"):
        return bool(value)
    if runtime.is_instance(value, "Date"):
        date = value.value
        return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"
    if isinstance(value, (str, int, float, bool, type(None), list, dict)):
        return value
    return str(value)
