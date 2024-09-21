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

def time_query(db_path, query):
    """Time the execution of a query on the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    start_time = time.time()  # Record the start time
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()  # Record the end time
    
    execution_time = end_time - start_time
    conn.close()
    
    return execution_time, result