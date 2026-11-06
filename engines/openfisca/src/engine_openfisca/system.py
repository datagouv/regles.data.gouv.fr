from functools import cache

from openfisca_core.scripts import build_tax_benefit_system
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.variables import Variable


@cache
def load_system(module: str) -> TaxBenefitSystem:
    """Load the tax and benefit system of a country package, such as `openfisca_france`."""
    return build_tax_benefit_system(module, None, None)


def variable(system: TaxBenefitSystem, name: str) -> Variable:
    found = system.get_variable(name)
    if found is None:
        raise ValueError(f"the system has no variable {name!r}")
    return found
