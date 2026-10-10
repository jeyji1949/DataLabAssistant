import pandas as pd


def average_curve(table, strain):
    one_strain = table[table["strain"] == strain]
    curve = one_strain.groupby("time_h")["od600"].mean()
    return curve


# Highest OD reached by the average curve
def peak_od(table, strain):
    curve = average_curve(table, strain)
    return float(curve.max())


def max_growth_rate(table, strain):
    curve = average_curve(table, strain)
    od_change = curve.diff()
    time_change = curve.index.to_series().diff()
    speed = od_change / time_change
    return float(speed.max())


def summary_table(table):
    rows = []
    for strain in sorted(table["strain"].unique()):
        rows.append({
            "strain": strain,
            "peak_od": round(peak_od(table, strain), 3),
            "max_growth_rate": round(max_growth_rate(table, strain), 3),
        })
    return pd.DataFrame(rows)


def fastest_strain(table):
    summary = summary_table(table)
    best_row = summary["max_growth_rate"].idxmax()
    return summary.loc[best_row, "strain"]