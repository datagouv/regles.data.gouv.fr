import datetime

from openfisca_core.indexed_enums import Enum
from openfisca_core.variables import Variable

SCHEMAS: dict[type, dict] = {
    float: {"type": "number"},
    int: {"type": "integer"},
    bool: {"type": "boolean"},
    str: {"type": "string"},
    datetime.date: {"type": "string", "format": "date"},
}
SAMPLES: dict[type, object] = {float: 0, int: 0, bool: False, str: "", datetime.date: "2000-01-01"}


def schema_of(variable: Variable) -> dict:
    """The JSON Schema of the value of a variable, titled by its label."""
    if variable.value_type is Enum:
        schema = {"oneOf": [{"const": item.name, "title": item.value} for item in variable.possible_values]}
    else:
        schema = dict(SCHEMAS[variable.value_type])
    return {**schema, "title": variable.label} if variable.label else schema


def sample_of(variable: Variable) -> object:
    if variable.value_type is Enum:
        return variable.default_value.name
    return SAMPLES[variable.value_type]
