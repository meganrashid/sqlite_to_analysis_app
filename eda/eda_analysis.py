""" EDA Analysis Done in eda.ipynb with markdown comments

This script executes the 
"""
import os
import subprocess


# # get the base directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# # get notebook paths
notebook_loc=  os.path.join(base_dir, 'eda', 'test.ipynb')

# # get output path
output_loc =  os.path.join(base_dir, 'output', 'test_results.ipynb')

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

# List of notebooks to execute
notebooks = [
    (notebook_loc, output_loc)
]

# Loop through and execute each notebook
for notebook_path, output_notebook_path in notebooks:
    if os.path.exists(notebook_path):
        run_notebook(notebook_path, output_notebook_path)
    else:
        print(f"Notebook not found: {notebook_path}")