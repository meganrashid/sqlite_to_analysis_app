# sqlite_to_analysis_app
 This application takes data from a sqlite db and outputs results of query results, EDA and analysis to a markdown file. 

## Overview
This application reads data from a SQLite database, performs exploratory data analysis (EDA), develops a model, and outputs the results to a markdown file.

### Requirements
- Python 3.x
- pandas
- scikit-learn
- sqlite3

### How to Run
1. Place your SQLite database in the `data/` folder.
2. Run the following command to generate the report:
   ```bash
   python scripts/generate_report.py

# Development Summary

## Setup
1. I created a Github repository to share my application and documentation.
2. The application's directory structure was setup using the following commands. 
'''
    # open project directory 
    cd sqlite_to_analysis_app

    # create subdirectories
    mkdir data eda model output scripts utils

    # create placeholder files in subdirectories. README.md already created from Github repo creation
    touch data/database.sqlite
    touch eda/eda_analysis.py
    touch model/model_dev.py
    touch output/results.md
    touch scripts/generate_report.py
    touch utils/db_utils.py
    touch utils/markdown_writer.py
    
    # reinitialize git repo 
    git init

    # add all newly created files to git
    git add .

    # commit the initial app structure
    git commit -m "Initial application structure setup"

    # create .gitignore file to exclude unnecessary files
    echo "output/results.md" >> .gitignore

    # add .gitignore file to git
    git add .gitignore
    git commit -m "add .gitignore"

    # link to repo
    https://github.com/meganrashid/sqlite_to_analysis_app
'''

## Inspect the data
1. 