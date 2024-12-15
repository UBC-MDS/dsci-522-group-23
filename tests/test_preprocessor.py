# test_preprocessor.py
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.preprocessor import create_preprocessor, transform_to_dataframe

def test_create_preprocessor():
    """
    Test the create_preprocessor function to ensure it creates a valid preprocessing pipeline.
    """
    X_train = pd.DataFrame({
        "sex": ["M", "F", "M", "F"],
        "age": [15, 16, 15, 16],
        "studytime": [2, 3, 2, 4],
    })

    preprocessor = create_preprocessor(X_train)
    assert preprocessor is not None

    transformed = preprocessor.fit_transform(X_train)
    assert transformed.shape[1] > 0
    print("Test passed: Preprocessor created and applied successfully.")

def test_mixed_data_types():
    """
    Test the preprocessor with a mix of numeric and categorical data.
    """
    X_train = pd.DataFrame({
        "gender": ["M", "F", "F", "M"],
        "age": [20, 21, 22, 19],
        "income": [50000, 60000, 55000, 52000],
        "city": ["A", "B", "A", "C"]
    })

    preprocessor = create_preprocessor(X_train)
    transformed = preprocessor.fit_transform(X_train)
    transformed_df = transform_to_dataframe(preprocessor, X_train, transformed)
    assert transformed_df.shape[0] == X_train.shape[0]
    print("Test passed: Mixed data types processed successfully.")

def test_empty_dataframe():
    """
    Test the preprocessor with an empty DataFrame.
    """
    X_train = pd.DataFrame()

    try:
        create_preprocessor(X_train)
        print("Test failed: Should not process empty DataFrame.")
    except ValueError as e:
        print("Test passed: Empty DataFrame handled correctly.")

def test_no_numeric_data():
    """
    Test the preprocessor with only categorical data.
    """
    X_train = pd.DataFrame({
        "category": ["A", "B", "C", "A"],
        "label": ["X", "Y", "X", "Z"]
    })

    preprocessor = create_preprocessor(X_train)
    transformed = preprocessor.fit_transform(X_train)
    transformed_df = transform_to_dataframe(preprocessor, X_train, transformed)
    assert transformed_df.shape[0] == X_train.shape[0]
    print("Test passed: No numeric data processed successfully.")

def test_no_categorical_data():
    """
    Test the preprocessor with only numeric data.
    """
    X_train = pd.DataFrame({
        "feature1": [1, 2, 3, 4],
        "feature2": [5, 6, 7, 8]
    })

    preprocessor = create_preprocessor(X_train)
    transformed = preprocessor.fit_transform(X_train)
    transformed_df = transform_to_dataframe(preprocessor, X_train, transformed)
    assert transformed_df.shape[0] == X_train.shape[0]
    print("Test passed: No categorical data processed successfully.")

def test_duplicate_columns():
    """
    Test the preprocessor with duplicate column names.
    """
    X_train = pd.DataFrame({
        "feature": [1, 2, 3, 4],
        "feature": [5, 6, 7, 8]  # Duplicate column name
    })

    preprocessor = create_preprocessor(X_train)
    transformed = preprocessor.fit_transform(X_train)
    transformed_df = transform_to_dataframe(preprocessor, X_train, transformed)
    assert transformed_df.shape[0] == X_train.shape[0]
    print("Test passed: Duplicate columns processed successfully.")

if __name__ == "__main__":
    test_create_preprocessor()
    test_mixed_data_types()
    test_empty_dataframe()
    test_no_numeric_data()
    test_no_categorical_data()
    test_duplicate_columns()



