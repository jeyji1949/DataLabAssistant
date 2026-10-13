import pandas as pd

from src.assistant import run_tool


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


def test_list_strains():
    result = run_tool("list_strains", {}, make_small_table())
    assert result == {"strains": ["strain_a", "strain_b"]}


def test_strain_summary():
    result = run_tool("get_strain_summary", {"strain": "strain_a"}, make_small_table())
    assert result["peak_od"] == 1.5
    assert result["max_growth_rate"] == 1.0


def test_unknown_strain_returns_error():
    result = run_tool("get_strain_summary", {"strain": "banana"}, make_small_table())
    assert "error" in result


def test_unknown_tool_returns_error():
    result = run_tool("do_magic", {}, make_small_table())
    assert "error" in result

def test_fastest_strain_includes_rate_and_unit():
    result = run_tool("get_fastest_strain", {}, make_small_table())
    assert result["fastest_strain"] == "strain_a"
    assert result["max_growth_rate"] == 1.0
    assert result["unit"] == "OD600 per hour"