import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.parsing import parse_plate_file
from src.schema import validate_rows
from src.storage import save_to_json, save_to_sqlite, load_from_sqlite
from src.analysis import summary_table, fastest_strain

table = parse_plate_file("data/raw/plate_run_01.csv")
good_rows, bad_rows = validate_rows(table)
print("Valid rows:", len(good_rows))

save_to_json(good_rows, "data/clean/plate_run_01.json")
save_to_sqlite(good_rows, "data/clean/lab.db")

clean_table = load_from_sqlite("data/clean/lab.db")
print(summary_table(clean_table))
print("Fastest strain:", fastest_strain(clean_table))