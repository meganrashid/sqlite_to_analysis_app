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

# get data path
db_path = os.path.join(base_dir, 'data', 'combined_data.db')

#connect to the database
conn = db.connect_to_db(db_path)

############################################ SQL QUERIES ####################################################
# get output directory
output_path = os.path.join(base_dir, 'output')
print(f"Query Results Will be Saved at: {output_path}")

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

