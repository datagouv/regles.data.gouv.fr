from engine_openfisca import periods
from engine_openfisca.rule import OpenfiscaRule, read_rule
from engine_openfisca.values import sample_of, schema_of


def input_schema_of(variable, rule: OpenfiscaRule) -> dict:
    if variable.name in rule.rolling_year_inputs:
        return {**schema_of(variable), "description": periods.ROLLING_YEAR_DESCRIPTION}
    return schema_of(variable)


def infer_call_contract(rule: OpenfiscaRule) -> dict:
    """Infer the input and output JSON Schemas of a rule, with a sample input."""
    _, outputs, inputs, unit = read_rule(rule)
    period = {"type": "string", "title": "Période", "description": periods.DESCRIPTIONS[unit], "pattern": periods.PATTERNS[unit]}
    input_schema = {
        "type": "object",
        # OpenFisca would compute with the default value of a missing input
        "required": ["period", *rule.inputs],
        "properties": {"period": period, **{item.name: input_schema_of(item, rule) for item in inputs}},
        "additionalProperties": False,
    }
    output_schema = {
        "type": "object",
        "required": list(rule.outputs),
        "properties": {item.name: schema_of(item) for item in outputs},
        "additionalProperties": False,
    }
    sample_input = {"period": periods.SAMPLES[unit], **{item.name: sample_of(item) for item in inputs}}
    return {"input_schema": input_schema, "output_schema": output_schema, "sample_input": sample_input, "warnings": []}
