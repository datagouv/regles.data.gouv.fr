from engine_openfisca import OpenfiscaRule

TEMPLATE = "openfisca_country_template"

PASS_CULTURE = OpenfiscaRule("openfisca_france", ("pass_culture",), ("date_naissance",))
# a monthly output of a person read from an eternal input
AGE = OpenfiscaRule(TEMPLATE, ("age",), ("birth",))
# a monthly output read from a yearly input
TOTAL_TAXES = OpenfiscaRule(TEMPLATE, ("total_taxes",), ("housing_tax",))
# a monthly output of a household read from an enumeration and a number of the household
HOUSING_ALLOWANCE = OpenfiscaRule(TEMPLATE, ("housing_allowance",), ("housing_occupancy_status", "rent"))

RULES = [PASS_CULTURE, AGE, TOTAL_TAXES, HOUSING_ALLOWANCE]

# each refused rule, with a part of the message that names the reason
REFUSED = {
    "unknown variable": (OpenfiscaRule(TEMPLATE, ("salary",), ("unknown",)), "no variable 'unknown'"),
    "outputs of two units": (OpenfiscaRule(TEMPLATE, ("salary", "housing_tax"), ()), "share one definition period"),
    "eternal output": (OpenfiscaRule(TEMPLATE, ("birth",), ()), "share one definition period"),
    "monthly input of a yearly rule": (OpenfiscaRule(TEMPLATE, ("housing_tax",), ("salary",)), "the input salary"),
}
