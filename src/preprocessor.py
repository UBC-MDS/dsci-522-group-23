# preprocessor.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer

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
    numeric_feats = X_train.select_dtypes(include=["int64"]).columns

    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(drop="if_binary", sparse_output=False), categorical_feats),
        verbose_feature_names_out=False,
    )
    return preprocessor
