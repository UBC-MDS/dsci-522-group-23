import os
import pandas as pd

def load_valid_data(filepath: str) -> pd.DataFrame:
    """
    Check filepath and load the correct file.

    Parameters
    ----------
    filepath : str
        Path to the file to load.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is not a CSV file.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")

    if not filepath.endswith(".csv"):
        raise ValueError(f"The file '{filepath}' is not a CSV file.")

    student_performance = pd.read_csv(filepath, delimiter=";")
    columns = ["sex", "age", "studytime", "failures", "goout", "Dalc", "Walc", "G3"]
    return student_performance[columns]