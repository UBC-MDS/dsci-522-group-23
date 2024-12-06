# split_n_preprocess.py

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
    Split the raw data into train and test sets.
    Preprocesses the data to be used in exploratory data analysis.
    Saves the preprocessor to be used in the model training script.
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

    preprocessor.fit(X_train)
    transformed_train = preprocessor.transform(X_train)
    transformed_test = preprocessor.transform(X_test)

    transformed_train.to_csv(
        os.path.join(data_to, "transformed_train.csv"), index=False
    )
    transformed_test.to_csv(os.path.join(data_to, "transformed_test.csv"), index=False)


if __name__ == "__main__":
    main()
