import sqlite3
import time

def connect_to_db(db_path):
    """Connect to SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn

def run_query(conn, query):
    """Run a SQL query and return the result."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def time_query(conn, query):
    """Time the execution of a query on the SQLite database."""
    cursor = conn.cursor()
    start_time = time.time()  # Record the start time
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()  # Record the end time
    
    execution_time = end_time - start_time
    
    return execution_time, result

def check_for_unnamed_columns(conn, table_name):
    """
    Identifies if there are any unnamed columns in the specified SQLite table.
    Returns:
        list: A list of column indexes that have no name.
    """

    cursor = conn.cursor()

    # Query the table info using PRAGMA
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()

    # List to store unnamed column indexes
    unnamed_columns = []

    # Iterate through the column info, checking for unnamed columns
    for column in columns_info:
        col_id, col_name, col_type, not_null, default_value, primary_key = column
        if not col_name:  # Check if the column name is empty or None
            unnamed_columns.append(col_id)

    return unnamed_columns

