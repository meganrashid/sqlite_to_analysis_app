import sqlite3
import time
import pandas as pd
import os


def connect_to_db(db_path):
    """Connect to SQLite database.

    Args:
    - db_path (str): path to database file

    Example: "C:/Users/megan/OneDrive/Documents/GitHub/sqlite_to_analysis_app/data/combined_data.db"
    """
    conn = sqlite3.connect(db_path)
    return conn

def run_query(conn, query):
    """Run a SQL query and return the result.
    
    Args:
    - db_path (str): path to database file

    Example: "C:/Users/megan/OneDrive/Documents/GitHub/sqlite_to_analysis_app/data/combined_data.db"
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def time_query(conn, query):
    """Time the execution of a query on the SQLite database.
    
    Args:
    - conn (str): connection string variable
    - query (str): string of SQLite query
    """
    cursor = conn.cursor()
    start_time = time.time()  # Record the start time
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()  # Record the end time
    
    execution_time = end_time - start_time
    
    return execution_time, result


# rename columns in table for development ease

def rename_columns(conn, table_name, columns_to_rename):
    """
    Create rename columns on SQLite tables based on the dictionary input.
    
    Args:
    - conn (str): connection to SQLite database file.
    - table_name (str): name of table to update
    - indexes_to_create (dict): A dictionary where keys are table names and values are lists of column names to index.
    
    Example:
    columns_to_rename = {
        'Unnamed: 0':'Company_ID",
        'size range':'size_range'
    }
    """
    cursor = conn.cursor()
    table = table_name
    
    # Iterate over the dictionary of current and updated column names
    for key,value in columns_to_rename.items():
        print(key, "-->", value)
        if ' ' in key:
        # SQL query to update the column name
            query = "ALTER TABLE {} RENAME COLUMN '{}'TO {}".format(table, key, value)
        else:
            # SQL query to update the column name
            query = "ALTER TABLE {} RENAME COLUMN {} TO {}".format(table, key, value)
            
        # Execute the query
        cursor.execute(query)
        # print(f"Updated name: {table} column changed from {key} to {value}")
    
    # Commit and close the connection
    conn.commit()

# add indexes

def create_indexes(conn, indexes_to_create):
    """
    Create indexes on SQLite tables based on the dictionary input.
    
    Args:
    - conn (str): connection to SQLite database file.
    - indexes_to_create (dict): A dictionary where keys are table names and values are lists of column names to index.
    
    Example:
   indexes_to_create = {
    'CompanyDataset': ['Company_ID','CompanyName', 'Website','industry','size range', 'country']
    ,'CompanyClassification': ['Category', 'CompanyName', 'Website']
    }
    """
    cursor = conn.cursor()
    
    # Iterate over the dictionary of tables and columns
    for table, columns in indexes_to_create.items():
        for column in columns:
            # Create index name based on table and column names
            index_name = f"idx_{table.lower()}_{column.lower()}"
            
            # SQL query to create the index if it doesn't already exist
            query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column});"
            
            # Execute the query
            cursor.execute(query)
            print(f"Created index: {index_name} on {table}({column})")
    
    # Commit
    conn.commit()



def query_to_excel(conn, output_dir, query, output_filename='query_results.xlsx'):
    """
    Runs a query on the SQLite database to pandas DF then saves the results to an Excel file in the output folder.
    
    Args:
    - conn (str): created from connect_to_db function
    - output_dir (str): path to output file directory
    - query (str): the SQL query to run.
    - output_filename (str): the filename for the output Excel file (default is 'query_results.xlsx').
    
    Returns:
    - str, path to the saved Excel file.
    """
    # Construct the path to the output folder
    # base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # output_dir = os.path.join(base_dir, 'output')
    # print(output_dir)
    
    # Run the query and fetch the result into a DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Ensure the output folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the full path for the output Excel file
    output_path = os.path.join(output_dir, output_filename)
    
    # Write the DataFrame to an Excel file
    df.to_excel(output_path, index=False)
    
    print(f"Query results successfully saved to: {output_path}")
    return output_path