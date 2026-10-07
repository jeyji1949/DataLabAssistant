import pandas as pd

table = pd.read_csv("data/raw/plate_run_01.csv")

print(table.head())        # first 5 rows
print(table.dtypes)        # type of each column
print(table["Sample"].unique())  # all strain names
