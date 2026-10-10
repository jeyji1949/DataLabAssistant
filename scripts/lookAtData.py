import pandas as pd

table = pd.read_csv("data/raw/plate_run_01.csv")

print(table.head())      
print(table.dtypes)        
print(table["Sample"].unique()) 
