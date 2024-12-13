# preprocessor.py
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

def create_preprocessor(X_train):
    """
    Creates a preprocessing pipeline for the given dataset.

    Parameters
    ----------
    X_train : pd.DataFrame
        Training features dataset.

    Returns
    -------
    preprocessor : sklearn.compose.ColumnTransformer
        A preprocessing pipeline with scaling and encoding steps.
    """
    categorical_feats = X_train.select_dtypes(include=["object"]).columns
    numeric_feats = X_train.select_dtypes(include=["int64", "float64"]).columns

    # Scaling and encoding pipeline
    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(drop="if_binary", sparse_output=False), categorical_feats),
        verbose_feature_names_out=True,  # Ensure unique feature names
    )
    return preprocessor

# Convert transformed output to a DataFrame for consistency
def transform_to_dataframe(preprocessor, X_train, transformed):
    """
    Converts the transformed output back to a DataFrame.

    Parameters
    ----------
    preprocessor : sklearn.compose.ColumnTransformer
        The preprocessor pipeline used for transformation.
    X_train : pd.DataFrame
        Original DataFrame before transformation.
    transformed : np.ndarray
        Transformed output from the preprocessor.

    Returns
    -------
    pd.DataFrame
        Transformed data as a DataFrame with appropriate feature names.
    """
    return pd.DataFrame(
        transformed,
        columns=preprocessor.get_feature_names_out(),
        index=X_train.index
    )








