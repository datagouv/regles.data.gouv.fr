from openfisca_core.periods import period

from engine_openfisca.periods import rolling_year


def test_the_rolling_year_is_the_twelve_months_before_the_requested_month():
    assert str(rolling_year(period("2025-03"))) == "year:2024-03"
