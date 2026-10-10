import pandas as pd
from src.parsing import fix_od_values


def test_text_becomes_missing_value():
    table = pd.DataFrame({"od600": ["0.5", "N/A", 0.7]})
    result = fix_od_values(table)

    assert result.loc[0, "od600"] == 0.5
    assert pd.isna(result.loc[1, "od600"])