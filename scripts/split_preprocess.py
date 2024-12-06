# split_n_preprocess.py
# Usage: python scripts/split_preprocess.py --raw-data=data/raw/student-mat.csv 
# --data-to=data/processed/ --preprocessor-to=results/models/

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder


@click.command()
@click.option("--raw-data", type=str, help="Path to validated data")
@click.option(
    "--data-to",
    type=str,
    help="Path to directory where processed data will be written to",
)
@click.option(
    "--preprocessor-to",
    type=str,
    help="Path to directory where the preprocessor object will be written to",
)
def main(raw_data, data_to, preprocessor_to):
    """
    Splits raw data into train and test sets, preprocesses the data, and saves the results for further use.

    The function performs the following tasks:
    1. Reads the raw student performance dataset.
    2. Splits the data into training and testing subsets.
    3. Saves the train/test splits as CSV files for exploratory data analysis.
    4. Creates and saves a preprocessing pipeline for use in downstream model training.

    Parameters
    ----------
    raw_data : str
        Path to the raw validated dataset (CSV format).
    data_to : str
        Directory path where the processed train and test datasets will be saved.
    preprocessor_to : str
        Directory path where the preprocessor object (pickle file) will be saved.

    Returns
    -------
    None
        The function saves the processed data and preprocessor object to the specified directories.

    Examples
    --------
    To execute this script via the command line:
    ```bash
    python scripts/split_preprocess.py \
        --raw-data='data/raw/student-mat.csv' \
        --data-to='data/processed/' \
        --preprocessor-to='results/models/'
    ```
    """

    set_config(transform_output="pandas")

    student_performance = pd.read_csv(raw_data, delimiter=";")

    # Necessary columns
    columns = ["sex", "age", "studytime", "failures", "goout", "Dalc", "Walc", "G1", "G2", "G3"]

    subset_df = student_performance[columns]

    # Split the dataset
    train_df, test_df = train_test_split(subset_df, test_size=0.2, random_state=123)
    print("Train-test split successful!")

    X_train, y_train = (train_df.drop(columns=["G3"]), train_df["G3"])
    X_test, y_test = (test_df.drop(columns=["G3"]), test_df["G3"])
    
    # saving X/y train/test to csv
    X_train.to_csv(os.path.join(data_to, "X_train.csv"), index=False)
    y_train.to_csv(os.path.join(data_to, "y_train.csv"), index=False)
    X_test.to_csv(os.path.join(data_to, "X_test.csv"), index=False)
    y_test.to_csv(os.path.join(data_to, "y_test.csv"), index=False)

    # Store splits in csv files
    os.makedirs(data_to, exist_ok=True)
    train_df.to_csv(os.path.join(data_to, "train_df.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "test_df.csv"), index=False)

    categorical_feats = X_train.select_dtypes(include=["object"]).columns
    numeric_feats = X_train.select_dtypes(include=["int64"]).columns

    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(drop="if_binary", sparse_output=False), categorical_feats),
        verbose_feature_names_out=False,
    )

    os.makedirs(preprocessor_to, exist_ok=True)
    pickle.dump(
        preprocessor, open(os.path.join(preprocessor_to, "preprocessor.pickle"), "wb")
    )

if __name__ == "__main__":
    main()
