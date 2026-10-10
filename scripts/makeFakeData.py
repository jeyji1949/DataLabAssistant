import math
import random
import pandas as pd

random.seed(42) 



def growth_curve(max_od, speed, midpoint):
    points = []
    time_h = 0.0
    while time_h <= 24:
        od = max_od / (1 + math.exp(-speed * (time_h - midpoint)))
        od = od + random.uniform(-0.02, 0.02)  
        points.append((time_h, round(od, 3)))
        time_h = time_h + 0.5
    return points


all_rows = []


def add_curve(sample_name, replicate, curve):
    for time_h, od in curve:
        all_rows.append([time_h, sample_name, replicate, od])

add_curve("Strain_A",  1, growth_curve(1.2, 0.5, 8))
add_curve("strain_a ", 2, growth_curve(1.2, 0.5, 8))
add_curve("STRAIN_A",  3, growth_curve(1.2, 0.5, 8))

add_curve("Strain_B",  1, growth_curve(1.0, 0.4, 10))
add_curve(" strain_b", 2, growth_curve(1.0, 0.4, 10))
add_curve("Strain_B",  3, growth_curve(1.0, 0.4, 10))

add_curve("Strain_C",  1, growth_curve(0.8, 0.3, 12))
add_curve("STRAIN_C",  2, growth_curve(0.8, 0.3, 12))
add_curve("strain_c",  3, growth_curve(0.8, 0.3, 12))


table = pd.DataFrame(
    all_rows,
    columns=["Time (h)", "Sample", "Rep #", "OD600 nm"],
)

table["OD600 nm"] = table["OD600 nm"].astype(object)
table.loc[10, "OD600 nm"] = None     
table.loc[200, "OD600 nm"] = "N/A"   


table.to_csv("data/raw/plate_run_01.csv", index=False)
print("Done! Rows saved:", len(table))
