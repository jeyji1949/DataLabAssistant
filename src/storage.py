import json
import sqlite3
import pandas as pd


def save_to_json(good_rows, path):
    data = []
    for row in good_rows:
        data.append(row.model_dump())  

    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def save_to_sqlite(good_rows, db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS measurements")
    cursor.execute("""
        CREATE TABLE measurements (
            strain TEXT,
            replicate INTEGER,
            time_h REAL,
            od600 REAL
        )
    """)

    for row in good_rows:
        cursor.execute(
            "INSERT INTO measurements VALUES (?, ?, ?, ?)",
            (row.strain, row.replicate, row.time_h, row.od600),
        )

    connection.commit()
    connection.close()


# Read everything back from the database as a pandas table
def load_from_sqlite(db_path):
    connection = sqlite3.connect(db_path)
    table = pd.read_sql_query("SELECT * FROM measurements", connection)
    connection.close()
    return table