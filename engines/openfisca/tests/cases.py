from engine_openfisca import OpenfiscaRule

TEMPLATE = "openfisca_country_template"

PASS_CULTURE = OpenfiscaRule("openfisca_france", ("pass_culture",), ("date_naissance",))
# a monthly output of a person read from an eternal input
AGE = OpenfiscaRule(TEMPLATE, ("age",), ("birth",))
# a monthly output read from a yearly input
TOTAL_TAXES = OpenfiscaRule(TEMPLATE, ("total_taxes",), ("housing_tax",))
# a monthly output of a household read from a number of the household
HOUSING_ALLOWANCE = OpenfiscaRule(TEMPLATE, ("housing_allowance",), ("rent",))
# an enumeration of a household, read and returned
OCCUPANCY = OpenfiscaRule(TEMPLATE, ("housing_occupancy_status",), ("housing_occupancy_status",))
# a text of a household, read and returned
POSTAL_CODE = OpenfiscaRule(TEMPLATE, ("postal_code",), ("postal_code",))

# the taxable salary read over the rolling year, as the request builder of aides simplifiées sets it
PRIME_ACTIVITE = OpenfiscaRule("openfisca_france", ("ppa",), ("salaire_imposable",), ("salaire_imposable",))

RULES = [PASS_CULTURE, AGE, TOTAL_TAXES, HOUSING_ALLOWANCE, OCCUPANCY, POSTAL_CODE, PRIME_ACTIVITE]

# the expected outputs of the pass culture come from tests/formulas/pass_culture.yaml of OpenFisca France 175.1.4
EXECUTIONS = [
    (PASS_CULTURE, {"period": "2025-04", "date_naissance": "2007-02-01"}, {"pass_culture": 150.0}),
    (PASS_CULTURE, {"period": "2025-04", "date_naissance": "1995-03-02"}, {"pass_culture": 0.0}),
    (AGE, {"period": "2025-04", "birth": "1990-01-01"}, {"age": 35}),
    (TOTAL_TAXES, {"period": "2025-04", "housing_tax": 1200}, {"total_taxes": 100.0}),
    (HOUSING_ALLOWANCE, {"period": "2015-01", "rent": 500.1}, {"housing_allowance": 125.025}),
    (OCCUPANCY, {"period": "2025-04", "housing_occupancy_status": "free_lodger"}, {"housing_occupancy_status": "free_lodger"}),
    (POSTAL_CODE, {"period": "2025-04", "postal_code": "75001"}, {"postal_code": "75001"}),
    (PRIME_ACTIVITE, {"period": "2025-03", "salaire_imposable": 12000}, {"ppa": 307.40826}),
]

UNREADABLE = [
    (PASS_CULTURE, {"period": "2025-04", "date_naissance": "2007-13-01"}),
    (HOUSING_ALLOWANCE, {"period": "2015-01", "rent": "abc"}),
    (OCCUPANCY, {"period": "2025-04", "housing_occupancy_status": "castle"}),
]

# each refused rule, with a part of the message that names the reason
REFUSED = {
    "unknown variable": (OpenfiscaRule(TEMPLATE, ("salary",), ("unknown",)), "no variable 'unknown'"),
    "outputs of two units": (OpenfiscaRule(TEMPLATE, ("salary", "housing_tax"), ()), "share one definition period"),
    "eternal output": (OpenfiscaRule(TEMPLATE, ("birth",), ()), "share one definition period"),
    "monthly input of a yearly rule": (OpenfiscaRule(TEMPLATE, ("housing_tax",), ("salary",)), "the input salary"),
    "rolling year input outside the inputs": (OpenfiscaRule(TEMPLATE, ("income_tax",), (), ("salary",)), "is not an input"),
    "yearly rolling year input": (OpenfiscaRule(TEMPLATE, ("total_taxes",), ("housing_tax",), ("housing_tax",)), "is not defined by month"),
    "rolling year input that copies its value": (
        OpenfiscaRule("openfisca_france", ("ppa",), ("livret_a",), ("livret_a",)),
        "does not divide its input",
    ),
}
