import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.parsing import parse_plate_file
from src.schema import Measurement, validate_rows

sys.path.append(str(Path(__file__).resolve().parent.parent))
table = parse_plate_file("data/raw/plate_run_01.csv")
print(table.head())
print(table["strain"].unique())

good_rows, bad_rows = validate_rows(table)
print("Valid rows:", len(good_rows))
print("Rejected rows:", len(bad_rows))

try:
    Measurement(strain="strain_a", replicate=1, time_h=2.0, od600=-3)
except Exception as error:
    print("Inspector says:", error)
