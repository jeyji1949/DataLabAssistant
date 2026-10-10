import pandas as pd
import pytest
from src.analysis import max_growth_rate, fastest_strain


# A tiny table: strain_a grows by 1.0 per hour at best, strain_b by only 0.2
def make_small_table():
    rows = [
        {"time_h": 0.0, "strain": "strain_a", "replicate": 1, "od600": 0.0},
        {"time_h": 1.0, "strain": "strain_a", "replicate": 1, "od600": 1.0},
        {"time_h": 2.0, "strain": "strain_a", "replicate": 1, "od600": 1.5},
        {"time_h": 0.0, "strain": "strain_b", "replicate": 1, "od600": 0.0},
        {"time_h": 1.0, "strain": "strain_b", "replicate": 1, "od600": 0.2},
        {"time_h": 2.0, "strain": "strain_b", "replicate": 1, "od600": 0.4},
    ]
    return pd.DataFrame(rows)


def test_max_growth_rate():
    table = make_small_table()
    assert max_growth_rate(table, "strain_a") == pytest.approx(1.0)
    assert max_growth_rate(table, "strain_b") == pytest.approx(0.2)


def test_fastest_strain():
    table = make_small_table()
    assert fastest_strain(table) == "strain_a"