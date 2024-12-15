import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_test(data, target_column, test_size=0.2, random_state=123):
    """
    Splits the input dataset into training and testing sets.
    
    Parameters:
    ----------
    data: pandas.DataFrame
        The input dataset.
    target_column: str
        Name of the target column to separate as y.
    test_size: float
        Proportion of data to include in the test split. Default is 0.2.
    random_state: int
        Random seed for reproducibility. Default is 123.
    
    Returns:
    --------
        tuple: 
            X_train, X_test, y_train, y_test.
    
    Raises:
    -------
    ValueError
        If the target column doesn't exist.
        If the test_size is not between 0 and 1.
    
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column {target_column} not found in dataset.")

    if test_size  < 0 or test_size > 1:
        raise ValueError(f"Test size {test_size} should range from 0 to 1")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

