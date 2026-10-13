import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from src.parsing import (
    read_raw_file,
    rename_columns,
    clean_strain_names,
    fix_od_values,
    drop_missing,
)
from src.schema import validate_rows
from src.analysis import summary_table, fastest_strain, all_average_curves


st.title("Lab Data Assistant")
st.write("Upload a raw plate-reader CSV file. The app cleans it, checks it, and shows the results.")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is None:
    st.info("Waiting for a file. Try data/raw/plate_run_01.csv")
    st.stop()  

raw_table = read_raw_file(uploaded_file)

expected_columns = ["Time (h)", "Sample", "Rep #", "OD600 nm"]
missing_columns = []
for column in expected_columns:
    if column not in raw_table.columns:
        missing_columns.append(column)

if len(missing_columns) > 0:
    st.error("This file is missing the columns: " + ", ".join(missing_columns))
    st.write("Columns found in your file:", list(raw_table.columns))
    st.stop()

st.subheader("1. Raw file (messy)")
st.dataframe(raw_table.astype(str).head(12))


table = rename_columns(raw_table)
table = clean_strain_names(table)
table = fix_od_values(table)
missing_count = int(table["od600"].isna().sum())
table = drop_missing(table)


good_rows, bad_rows = validate_rows(table)

st.subheader("2. Quality report")
col1, col2, col3 = st.columns(3)
col1.metric("Rows in file", len(raw_table))
col2.metric("Removed (missing)", missing_count)
col3.metric("Rejected by schema", len(bad_rows))

if len(good_rows) == 0:
    st.error("No valid rows left after cleaning.")
    st.stop()

# Turn the valid rows back into a table
clean_data = []
for row in good_rows:
    clean_data.append(row.model_dump())
clean_table = pd.DataFrame(clean_data)


st.subheader("3. Average growth curves")
st.line_chart(all_average_curves(clean_table))

st.subheader("4. Summary per strain")
st.dataframe(summary_table(clean_table))

st.success("Fastest strain: " + str(fastest_strain(clean_table)))