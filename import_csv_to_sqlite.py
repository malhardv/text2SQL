import os
import sqlite3
import pandas as pd
import argparse

def build_database(csv_dir: str, sql_file: str, db_path: str):
    """
    Creates tables based on a provided .sql schema file, 
    and then imports CSV data into them using pandas.
    """
    if not os.path.exists(sql_file):
        print(f"Error: Schema file '{sql_file}' does not exist.")
        return
        
    if not os.path.isdir(csv_dir):
        print(f"Error: CSV Directory '{csv_dir}' does not exist.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Connected to SQLite database at {db_path}")

    # 1. Execute the SQL Schema
    print(f"Building tables from schema '{sql_file}'...")
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
        print("Schema loaded successfully!")
    except Exception as e:
        print(f"Failed to execute schema script: {e}")
        conn.close()
        return

    # 2. Iterate over CSVs and import data natively
    files_imported = 0
    for filename in os.listdir(csv_dir):
        if filename.endswith(".csv"):
            csv_path = os.path.join(csv_dir, filename)
            table_name = os.path.splitext(filename)[0]
            
            try:
                print(f"Importing {filename} into table '{table_name}'...")
                df = pd.read_csv(csv_path)
                
                # We use if_exists="append" because the tables establish 
                # columns, primary keys, and data types via the .sql file first!
                df.to_sql(table_name, conn, if_exists="append", index=False)
                
                print(f"  -> Successfully imported {len(df)} rows into '{table_name}'.")
                files_imported += 1
            except Exception as e:
                print(f"Failed to import {filename}: {e}")

    conn.close()
    print(f"\nImport complete! {files_imported} CSV files loaded into {db_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build SQLite DB using a .sql schema and fill with CSVs.")
    parser.add_argument("sql_file", help="Path to the .sql schema file")
    parser.add_argument("csv_folder", help="Path to the folder containing the CSV files")
    parser.add_argument("--db", default="test.db", help="Path to the output SQLite database (default: test.db)")
    
    args = parser.parse_args()
    build_database(args.csv_folder, args.sql_file, args.db)
