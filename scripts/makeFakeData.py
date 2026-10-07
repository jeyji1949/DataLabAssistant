import math
import random
import pandas as pd

random.seed(42)  # same "random" numbers every time


# Piece 1: one growth curve
# max_od   = how cloudy it gets at the end
# speed    = how fast it grows
# midpoint = the hour when growth is at its fastest
def growth_curve(max_od, speed, midpoint):
    points = []
    time_h = 0.0
    while time_h <= 24:
        od = max_od / (1 + math.exp(-speed * (time_h - midpoint)))
        od = od + random.uniform(-0.02, 0.02)  # small measurement noise
        points.append((time_h, round(od, 3)))
        time_h = time_h + 0.5  # one measurement every 30 minutes
    return points


# Piece 2: a place to collect all rows
all_rows = []


# Piece 3: add one curve to the collection
def add_curve(sample_name, replicate, curve):
    for time_h, od in curve:
        all_rows.append([time_h, sample_name, replicate, od])


# Piece 4: the 9 curves, written one by one
# Strain A grows fast, B medium, C slowly.
# The names are messy on purpose (capital letters, spaces).
add_curve("Strain_A",  1, growth_curve(1.2, 0.5, 8))
add_curve("strain_a ", 2, growth_curve(1.2, 0.5, 8))
add_curve("STRAIN_A",  3, growth_curve(1.2, 0.5, 8))

add_curve("Strain_B",  1, growth_curve(1.0, 0.4, 10))
add_curve(" strain_b", 2, growth_curve(1.0, 0.4, 10))
add_curve("Strain_B",  3, growth_curve(1.0, 0.4, 10))

add_curve("Strain_C",  1, growth_curve(0.8, 0.3, 12))
add_curve("STRAIN_C",  2, growth_curve(0.8, 0.3, 12))
add_curve("strain_c",  3, growth_curve(0.8, 0.3, 12))


# Piece 5: build the table with ugly column names
table = pd.DataFrame(
    all_rows,
    columns=["Time (h)", "Sample", "Rep #", "OD600 nm"],
)

# Piece 6: add some real-life problems
table["OD600 nm"] = table["OD600 nm"].astype(object)
table.loc[10, "OD600 nm"] = None     # a missing value
table.loc[200, "OD600 nm"] = "N/A"   # text where a number should be


# Piece 7: save the file
table.to_csv("data/raw/plate_run_01.csv", index=False)
print("Done! Rows saved:", len(table))
