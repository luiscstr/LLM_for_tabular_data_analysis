import pandas as pd
import sqlite3
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import os


def load_and_save_file(file):
    # Determine file type and load accordingly
    if file.name.endswith('.csv'):
        df = pd.read_csv(file.name)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        df = pd.read_excel(file.name)
    else:
        return "Unsupported file format", None

    # Generate database filename
   
    db_filename = "sqldb.db"

    # Check if database already exists
    if os.path.exists('./data/'+ db_filename):
        try:
            os.remove('./data/'+ db_filename)  # Remove the existing database
        except PermissionError:
            return f"Cannot replace the database '{db_filename}' because it is being used by another process.", None
    
    # Save DataFrame to SQLite database
    engine=create_engine(f"sqlite:///data/sqldb.db")
    df.to_sql(name="data", con=engine, if_exists="replace", index=False)
    engine.dispose()

    return f"Database '{db_filename}' has been created successfully.", df

#def handle_file_upload(file, db_name, replace=False):
#    # Ensure a database name is provided
#    if not db_name:
#        return "Please provide a database name.", None

#    return load_and_save_file(file, db_name, replace)