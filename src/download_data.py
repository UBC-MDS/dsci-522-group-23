import requests
from pathlib import Path
import os
import sys
import zipfile
import shutil

url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"

def download_data():
    
    script_path = os.path.dirname(os.path.abspath(__file__))
    zip_dir = Path(script_path, "..", "data", "zip")
    zip1 = os.path.join(zip_dir, "student_performance.zip")
    zip2 = os.path.join(zip_dir, "student.zip")
    dest_path = Path(script_path, "..", "data", "raw")
    
    if os.path.exists(os.path.join(dest_path, "student-mat.csv")):
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
    file_path = os.path.join(zip_dir, "student-mat.csv")
    shutil.copy(file_path, dest_path)

if __name__ == "__main__":
    download_data()