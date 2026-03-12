import os
import sqlite3
import pandas as pd

def build_database(csv_files: list[str], sql_file: str, db_path: str = "test.db"):
    """
    Creates tables based on a provided .sql schema file, 
    and then imports CSV data into them using pandas.
    """
    if not os.path.exists(sql_file):
        raise FileNotFoundError(f"Schema file '{sql_file}' does not exist.")

    # Remove the old database file if it exists so we start fresh
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError as e:
            raise Exception(f"Could not remove old database {db_path}. Is it open in another program? {e}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Execute the SQL Schema
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
    except Exception as e:
        conn.close()
        raise Exception(f"Failed to execute schema script: {e}")

    # 2. Iterate over provided CSV files and import data
    files_imported = 0
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            continue
            
        # Extract filename without extension for table name
        basename = os.path.basename(csv_file)
        table_name = os.path.splitext(basename)[0]
        
        try:
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            files_imported += 1
        except Exception as e:
            # We log it but continue
            print(f"Failed to import {csv_file}: {e}")

    conn.close()
    return files_imported
