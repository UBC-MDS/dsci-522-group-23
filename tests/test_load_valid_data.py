import pytest
import pandas as pd
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_valid_data import load_valid_data

@pytest.fixture
def sample_csv(tmp_path):
    """Fixture to create a sample CSV file for testing."""
    test_file = tmp_path / "students-math.csv"
    df = pd.DataFrame({
        "sex": ["F", "M", "F"],
        "age": [15, 16, 17],
        "studytime": [2, 3, 1],
        "failures": [0, 1, 0],
        "goout": [3, 2, 4],
        "Dalc": [1, 2, 1],
        "Walc": [2, 4, 5],
        "G3": [10, 12, 14]
    })
    df.to_csv(test_file, sep=";", index=False)
    return str(test_file)


def test_load_data_valid_csv(sample_csv):
    load_df = load_valid_data(sample_csv)
    expected_columns = ["sex", "age", "studytime", "failures", "goout", "Dalc", "Walc", "G3"]
    expected_dtypes = {
        "sex": "object",
        "age": "int64",
        "studytime": "int64",
        "failures": "int64",
        "goout": "int64",
        "Dalc": "int64",
        "Walc": "int64",
        "G3": "int64"
    }
    
    # Test column names
    assert list(load_df.columns) == expected_columns

    # Test column shape
    assert load_df.shape == (3, 8)

    # Test for null values
    assert load_df.isnull().sum().sum() == 0

    # Test for duplicate rows
    assert load_df.duplicated().sum() == 0

    # Test unique values in sex column
    assert set(load_df["sex"]) == {"F", "M"}

    # Test data types of each column
    for column, dtype in expected_dtypes.items():
        assert load_df[column].dtype == dtype


def test_load_data_file_not_found(tmp_path):
    # Create a temporary path to csv file with wrong name
    non_existent_file = tmp_path / "students-eng.csv"
    
    with pytest.raises(FileNotFoundError):
        load_valid_data(str(non_existent_file))


def test_load_data_not_csv(tmp_path):
    # Create a temporary path to a text file
    txt_file = tmp_path / "students-math.txt"
    txt_file.touch()
    
    with pytest.raises(ValueError):
        load_valid_data(str(txt_file))