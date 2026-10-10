import pandas as pd

def read_raw_file(path):
    table = pd.read_csv(path)
    return table


def rename_columns(table):
    table = table.rename(columns={
        "Time (h)": "time_h",
        "Sample": "strain",
        "Rep #": "replicate",
        "OD600 nm": "od600",
    })
    return table


def clean_strain_names(table):
    table["strain"] = table["strain"].str.strip().str.lower()
    return table


def fix_od_values(table):
    table["od600"] = pd.to_numeric(table["od600"], errors="coerce")
    return table


def drop_missing(table):
    table = table.dropna(subset=["od600"])
    return table


# Run all the steps in order
def parse_plate_file(path):
    table = read_raw_file(path)
    table = rename_columns(table)
    table = clean_strain_names(table)
    table = fix_od_values(table)

    rows_before = len(table)
    table = drop_missing(table)
    rows_removed = rows_before - len(table)
    print("Rows removed because of missing values:", rows_removed)

    return table
