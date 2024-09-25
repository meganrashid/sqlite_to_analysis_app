# sqlite_to_analysis_app
 This application takes data from a sqlite db and: 
 1. outputs results of query results to Excel files
 2. Run EDA notebook
 3. Creates a Logistic Regression model based on Distilbert embeddings

## Overview
This application reads data from a SQLite database, performs exploratory data analysis (EDA), develops a model, and outputs the results to a markdown file.

### Directory
```bash
sqlite_to_analysis_app/
│
├── data/
│   └── combined_data.db (sqlite database)
│
├── eda/
│   └── eda_analysis.py
│
├── model/
│   └── model_dev.py
│
├── output/
│   └── results.md          # results of queries saved to excel files here
│
├── scripts/
│   └── clean_data.py  # cleans database and creates new merged table for modeling
│   └── generate_report.py  # run SQL queries, save outputs to excel files
│
├── utils/
│   └── __init__.py
│   └── db_utils.py         # contains the database utility functions
│
└── README.md
```

### How to Run
1. Place your SQLite database in the `data/` folder. Must contain the tables CompanyDataset and CompanyClassification
2. Run the following command to generate the report:
```bash
   python scripts/generate_report.py
```


# Development Summary

## Setup
1. I created a Github repository to share my application and documentation.
2. The application's directory structure was setup using the following commands. 
```bash
    ### open project directory 
    cd sqlite_to_analysis_app

    ### create subdirectories
    mkdir data eda model output scripts utils

    ### create placeholder files in subdirectories. README.md already created from Github repo creation
    touch data/database.sqlite
    touch eda/eda_analysis.py
    touch model/model_dev.py
    touch output/results.md
    touch scripts/clean_data.py
    touch scripts/generate_report.py
    touch utils/db_utils.py
    touch utils/markdown_writer.py
    
    ### reinitialize git repo 
    git init

    ### add all newly created files to git
    git add .

    ### commit the initial app structure
    git commit -m "Initial application structure setup"

    ### create .gitignore file to exclude unnecessary files
    echo "output/results.md" >> .gitignore

    ### add .gitignore file to git
    git add .gitignore
    git commit -m "add .gitignore"

    ### link to repo
    https://github.com/meganrashid/sqlite_to_analysis_app
```

## Inspect the data
You can follow my thought process and steps to clean the data in the data\database_check.ipynb notebook.

## Task 1: SQL Queries
This is done while running generate_reports.py. Results of queries are saved to Excel files under the output folder.

## Task 2: Data Integration and Database Insertion
I rename columns, add indexes, create a new table CompanyMerged and insert results of query into that table in clean_data.py.

## Task 3: EDA & Text Preprocessing
EDA and text normalization done by running notebook eda.ipynb. Results of notebook saved to output folder.

## Task 4: Model Development
Logistic Regression trained on DistilBERT embeddings was chosen. However, the model was trained on 5000 records (dataset contains
71k) due to machine limitations. 

The full development process is outlined in model_dev.ipynb. This application is shipped with precomputed DistilBERT embeddings to support
faster model training.

## Task 5: Reporting
Full findings can be found in Report_Findings.md

Credits:
Text processing functions found in db_utils optimized from the work done by: https://github.com/robsalgado/personal_data_science_projects/commits?author=robsalgado