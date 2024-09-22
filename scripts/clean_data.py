import os
import sys
import pandas as pd

# Construct the absolute path to the utils directory and append it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

# Now you can import the db_utils module
import db_utils as db

# set up params

# get the base directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"base directory: {base_dir}")

# get data path
db_path = os.path.join(base_dir, 'data', 'combined_data.db')
print(f"Database path: {db_path}")

# get output directory
output_path = os.path.join(base_dir, 'output')
print(f"Query Results Will be Saved at: {output_path}")


#connect to the database
conn = db.connect_to_db(db_path)

# check table structure and column names


#rename columns
columns_to_rename = {'Unnamed: 0':'Company_ID',
                     'year founded':'Year_Founded',
                     'industry':'Industry',
                     'size range':'Size_Range',
                     'locality':'Locality',
                     'country':'Country',
                     'linkedin url': 'Linkedin_URL',
                     'current employee estimate':'Current_Employee_Estimate',
                     'total employee estimate':'Total_Employee_Estimate'
                     }

db.rename_columns(conn, 'CompanyDataset', columns_to_rename)

# add indexes to both tables
indexes_to_create = {
    'CompanyDataset': ['Company_ID','CompanyName', 'Website','Industry','Size_Range', 'Country','Current_Employee_Estimate','Total_Employee_Estimate']
    ,'CompanyClassification': ['Category', 'CompanyName', 'Website']
}

db.create_indexes(conn, indexes_to_create)

# check table structure and column names
print(db.run_query(conn,"PRAGMA table_info('CompanyDataset');"))

# create new table for modeling
db.run_query(conn, '''
                    CREATE TABLE IF NOT EXISTS CompanyMerged (
                     Company_ID INTEGER PRIMARY KEY
                     ,CompanyName TEXT NOT NULL
                     ,Website TEXT NOT NULL
                     ,Industry TEXT
                     ,Size_Range TEXT
                     ,Category TEXT NOT NULL
                     ,homepage_text TEXT NOT NULL
                     ,h1 TEXT
                     ,h2 TEXT
                     ,h3 TEXT
                     ,nav_link_text TEXT
                     ,meta_keywords TEXT
                     ,meta_description TEXT
                    )
                    '''
             )

# insert merged data from companyDataset and CompanyClassification to new table
db.run_query(conn, '''
                    INSERT INTO CompanyMerged
                    SELECT 
                        cd.Company_ID
                        ,cd.CompanyName
                        ,cd.Website
                        ,cd.Industry
                        ,cd.Size_Range
                        ,cc.Category
                        ,cc.homepage_text
                        ,cc.h1
                        ,cc.h2
                        ,cc.h3
                        ,cc.nav_link_text
                        ,cc.meta_keywords
                        ,cc.meta_description
                    FROM CompanyDataset as cd
                    INNER JOIN CompanyClassification as cc
                        ON cd.Website=cc.Website
                        and cc.Website is not null
                    WHERE cd.Website is not null
                    and cd.CompanyName is not null
                    and cc.homepage_text is not null
                    ''')




# create indexes for new table
indexes_to_create = {
    'CompanyMerged': ['Company_ID','CompanyName', 'Website','Industry','Category']
}

db.create_indexes(conn, indexes_to_create)

print("Table ready for preprocessing and modeling")