import os
import sys
import pandas as pd
import subprocess

# Construct the absolute path to the utils directory and append it to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))

# Only add the utils_path if it's not already in sys.path
if utils_path not in sys.path:
    sys.path.append(utils_path)

# Now you can import the db_utils module
import db_utils as db

###################################### set up params #######################################################

# get the base directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# get data path
db_path = os.path.join(base_dir, 'data', 'combined_data.db')

################################# functions to run scripts and notebooks ###################################

def run_clean_data_script():
    """
    Execute the clean_data.py script located in the scripts folder.
    """
    # Get the absolute path to the clean_data.py script
    clean_data_script = os.path.join(base_dir,'scripts','clean_data.py')
    
    try:
        # Execute the clean_data.py script using subprocess
        result = subprocess.run(['python', clean_data_script], check=True, capture_output=True, text=True)
        
        # If the script runs successfully, print the output
        print("clean_data.py script output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running clean_data.py: {e}")
        print(e.stderr)

def run_notebook(notebook_path, output_notebook_path):
    """
    Execute a Jupyter notebook and save the output.
    
    Args:
    - notebook_path: str, path to the notebook to execute.
    - output_notebook_path: str, path to save the executed notebook.
    
    Raises:
    - CalledProcessError if the subprocess fails.
    """
    try:
        command = f"jupyter nbconvert --to notebook --execute --output {output_notebook_path} {notebook_path}"
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {notebook_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {notebook_path}: {e}")
        raise

def run_model_dev_script():
    """
    Execute the clean_data.py script located in the scripts folder.
    """
    # Get the absolute path to the clean_data.py script
    model_dev_script = os.path.join(base_dir,'model','model_dev.py')
    
    try:
        # Execute the clean_data.py script using subprocess
        result = subprocess.run(['python', model_dev_script], check=True, capture_output=True, text=True)
        
        # If the script runs successfully, print the output
        print("clean_data.py script output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running clean_data.py: {e}")
        print(e.stderr)

######################################### Clean the database ################################################ 

if __name__ == "__main__":
    run_clean_data_script()

############################################ SQL QUERIES ####################################################
# get output directory
output_path = os.path.join(base_dir, 'output')
print(f"Query Results Will be Saved at: {output_path}")

#connect to the database
conn = db.connect_to_db(db_path)

# 1.  Find the Top 10 industries with the highest average number of employees, only considering companies
# founded after 2000 that have more than 10 employees
top_total_query = '''
            SELECT 
                cd.Industry
                ,AVG(cd.Current_Employee_Estimate)      as 'AVG_Current_Employee'
                ,AVG(cd.Total_Employee_Estimate)        as 'AVG_Total_Employee'
            FROM CompanyDataset as cd
            WHERE cd.Year_Founded > 2000
            AND cd.Size_Range <> '1 - 10'
            GROUP BY cd.Industry
            ORDER BY 3 desc
            LIMIT 10
        '''
output_dir = 'C:/Users/megan/OneDrive/Documents/GitHub/sqlite_to_analysis_app/output'

db.query_to_excel(conn, output_dir, top_total_query, output_filename='top_industries_by_total_avg_employees.xlsx')


top_current_query = '''
            SELECT 
                cd.Industry
                ,AVG(cd.Current_Employee_Estimate)      as 'AVG_Current_Employee'
                ,AVG(cd.Total_Employee_Estimate)        as 'AVG_Total_Employee'
            FROM CompanyDataset as cd
            WHERE cd.Year_Founded > 2000
            AND cd.Size_Range <> '1 - 10'
            GROUP BY cd.Industry
            ORDER BY 2 desc
            LIMIT 10
        '''
output_dir = 'C:/Users/megan/OneDrive/Documents/GitHub/sqlite_to_analysis_app/output'

db.query_to_excel(conn, output_dir, top_current_query, output_filename='top_industries_by_current_avg_employees.xlsx')

# 2. Idenitify companies in the 'Technology'-like industry that do not have effective homepage_text and have
# fewer than 100 employees based on data merged from both datasets

bad_homepage_text = '''
                        SELECT DISTINCT
                            cc.Category
                            ,cd.Industry
                            ,cd.CompanyName
                            --,cd.Website
                            --,cc.homepage_text
                        FROM CompanyDataset as cd
                        LEFT JOIN CompanyClassification as cc
                            ON cd.Website=cc.Website
                            and cc.Website is not null
                        WHERE cd.Website is not null
                        and cd.CompanyName is not null
                        and cd.Total_Employee_Estimate < 100
                        and cc.homepage_text is null
                        and cc.Category like '%technology%'
                    '''

db.query_to_excel(conn, output_dir, bad_homepage_text, output_filename='tech_companies_with_ineffective_homepage_text.xlsx')

# 3. Rank companies within each country by their total employee estimate in descending order, showing only companies that rank in the top 5 within their country. 
top5_country = '''
                with country_rank as (SELECT 
                                        cd.Country
                                        ,cd.CompanyName
                                        ,cd.Total_Employee_Estimate
                                        ,row_number() over( partition by cd.Country order by cd.Total_Employee_Estimate desc)   RowNum
                                    FROM CompanyDataset as cd
                                    WHERE cd.Country is not null
                                    and cd.CompanyName is not null
                                    )
                SELECT *
                FROM country_rank 
                where RowNum <6                       
                '''

db.query_to_excel(conn, output_dir, top5_country, output_filename='top_companies_per_country_total_employees.xlsx')

############################################ Run EDA & Create Text Database for Modeling ####################################################

# If you only want to run the eda.ipynb, you can run this using eda.py

print("Begin EDA --> ... ")

eda_notebook = os.path.join(base_dir, 'eda', 'eda.ipynb')
eda_output = os.path.join(base_dir, 'output', 'eda_results.ipynb')

# List of notebooks to execute
notebooks = [
    (eda_notebook, eda_output)
]

# Loop through and execute each notebook
for notebook_path, output_notebook_path in notebooks:
    if os.path.exists(notebook_path):
        run_notebook(notebook_path, output_notebook_path)
    else:
        print(f"Notebook not found: {notebook_path}")

############################################ Create the Model ####################################################

if __name__ == "__main__":
    run_model_dev_script()