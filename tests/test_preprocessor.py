# test_preprocessor.py
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.preprocessor import create_preprocessor

def test_create_preprocessor():
    """
    Test the create_preprocessor function to ensure it creates a valid preprocessing pipeline.
    """
    # Create a sample DataFrame
    X_train = pd.DataFrame({
        "sex": ["M", "F", "M", "F"],
        "age": [15, 16, 15, 16],
        "studytime": [2, 3, 2, 4],
    })

    # Call the function
    preprocessor = create_preprocessor(X_train)

    # Ensure the preprocessor is not None
    assert preprocessor is not None

    # Fit and transform to ensure it works
    transformed = preprocessor.fit_transform(X_train)

    # Check the shape of the transformed output
    assert transformed.shape[1] > 0
    print("Test passed: Preprocessor created and applied successfully.")

if __name__ == "__main__":
    test_create_preprocessor()
