""" 
python scripts/download_data.py \
    --url='https://archive.ics.uci.edu/static/public/320/student+performance.zip' \
    --out-dir='data/raw' \
    --raw-filename='student-mat.csv'
"""

import requests
from pathlib import Path
import os
import sys
import zipfile
import shutil
import click

# url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"

@click.command()
@click.option("--url", type=str, help="Data download URL")
@click.option(
    "--out-dir", type=str, 
    help="Output directory for the raw file, relative to the location of the script"
)
@click.option("--raw-filename", type=str, help="The raw data file name")
@click.option('--force', is_flag=True, help='Download the data forcefully without checking if file exists')
def download_uci_data(url, out_dir, raw_filename, force):
    
    """
    Downloads and extracts a dataset from a given URL, saving the raw data file to a specified directory.

    Parameters
    ----------
    url : str
        The URL from which to download the dataset (expected to be a ZIP file).
    out_dir : str
        The relative path to the directory where the raw data file should be saved.
    raw_filename : str
        The name of the raw data file to be extracted and saved.
    force : bool
        If True, forces a download and overwrite even if the file already exists.

    Returns
    -------
    None
        This function does not return a value. It downloads, extracts, and saves the specified data file.

    Examples
    --------
    Run the script via the command line:
    ```bash
    python scripts/download_data.py \
        --url='https://archive.ics.uci.edu/static/public/320/student+performance.zip' \
        --out-dir='data/raw' \
        --raw-filename='student-mat.csv'
    ```
    """

    script_path = os.path.dirname(os.path.abspath(__file__))
    zip_dir = Path(script_path, "..", "data", "zip")
    zip1 = os.path.join(zip_dir, "student_performance.zip")
    zip2 = os.path.join(zip_dir, "student.zip")
    dest_path = Path(script_path, "..", out_dir)
    
    if (not force) and os.path.exists(os.path.join(dest_path, raw_filename)):
        print("File already existed, exitting script...")
        sys.exit()
    
    response = requests.get(url, stream=True)
    print(os.getcwd())
    with open(zip1, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
        print(f"File downloaded successfully.")
    
    # Extract the outer zip file (student_performance.zip)
    with zipfile.ZipFile(zip1, "r") as zip_ref:
        zip_ref.extractall(zip_dir)
    # Extract the inner zip file (student.zip)
    with zipfile.ZipFile(zip2, "r") as zip_ref:
        zip_ref.extractall(zip_dir)
    
    # copy the file to data/raw
    file_path = os.path.join(zip_dir, raw_filename)
    shutil.copy(file_path, dest_path)

if __name__ == "__main__":
    download_uci_data()