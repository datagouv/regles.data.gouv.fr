import numpy
from openfisca_core.periods import DateUnit
from openfisca_core.scripts import build_tax_benefit_system
from openfisca_core.variables import Variable

from engine_openfisca.system import load_system
from engine_openfisca.values import sample_of, schema_of, to_json


def test_a_boolean_variable_is_a_json_boolean():
    # a system of its own: the systems of engine_openfisca.system are cached and shared by the tests
    system = build_tax_benefit_system("openfisca_country_template", None, None)

    class is_student(Variable):
        value_type = bool
        entity = system.person_entity
        definition_period = DateUnit.MONTH
        label = "Student"

    system.add_variable(is_student)
    variable = system.get_variable("is_student")

    assert schema_of(variable) == {"type": "boolean", "title": "Student"}
    assert sample_of(variable) is False
    assert to_json(numpy.array([True]), variable) is True


def test_a_date_is_written_in_iso_8601():
    birth = load_system("openfisca_country_template").get_variable("birth")

    assert to_json(numpy.array(["2007-02-01"], dtype="datetime64[D]"), birth) == "2007-02-01"
