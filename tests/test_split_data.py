import pandas as pd
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_data import split_train_test

# Fixture for generating test data
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [6, 7, 8, 9, 10],
        "target": [0, 1, 0, 1, 0]
    })


def test_split_train_test_basic(sample_data):
    X_train, X_test, y_train, y_test = split_train_test(sample_data, "target", test_size=0.4, random_state=42)
    
    # Check that the splits have the correct sizes
    assert len(X_train) == 3
    assert len(X_test) == 2
    assert len(y_train) == 3
    assert len(y_test) == 2
    
    # Ensure no data is lost
    assert len(X_train) + len(X_test) == len(sample_data)
    assert len(y_train) + len(y_test) == len(sample_data)


def test_split_train_test_column_integrity(sample_data):
    X_train, X_test, _, _ = split_train_test(sample_data, "target")
    # Ensure no columns are dropped from X
    assert list(X_train.columns) == ["A", "B"]
    assert list(X_test.columns) == ["A", "B"]


def test_split_train_test_invalid_target(sample_data):
    with pytest.raises(ValueError):
        split_train_test(sample_data, "nonexistent_column")


def test_split_train_test_invalid_test_size(sample_data):
    with pytest.raises(ValueError):
        split_train_test(sample_data, "target", test_size=1.5)
    with pytest.raises(ValueError):
        split_train_test(sample_data, "target", test_size=-0.5)



