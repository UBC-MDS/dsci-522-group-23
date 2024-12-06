# split_n_preprocess.py

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector


@click.command()
@click.option('--val-data', type=str, help="Path to validated data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
        
def main(raw_data, data_to, preprocessor_to):
    '''
    Split the raw data into train and test sets. 
    Preprocesses the data to be used in exploratory data analysis.
    Saves the preprocessor to be used in the model training script.
    '''
    set_config(transform_output="pandas")
    
    student_performance = load_data(raw_data)

    # Necessary columns
    columns = ['sex', 
               'age', 
               'studytime', 
               'failures', 
               'goout', 
               'Dalc', 
               'Walc',  
               'G3']
    
    subset_df = student_performance[columns]

    try:
        # Validate the data schema
        validate_student_data(subset_df)

        # Validate missingness in the dataset
        validate_missingness(subset_df, threshold=0.1, plot-to)

        # Validate target distribution
        validate_target_distribution(subset_df, plot-to)
        
    except ValueError as ve:
        print(f"Validation error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Split the dataset
        train_df, test_df = train_test_split(
            subset_df, test_size=0.2, random_state=123
        )
        print("Train-test split successful!")

    # Store splits in csv files
    train_df.to_csv(os.path.join(data_to, "train_df.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "test_df.csv"), index=False)

    cancer_preprocessor = make_column_transformer(
        (StandardScaler(), make_column_selector(dtype_include='number')),
        remainder='passthrough',
        verbose_feature_names_out=False
    )
    pickle.dump(cancer_preprocessor, open(os.path.join(preprocessor_to, "cancer_preprocessor.pickle"), "wb"))

    cancer_preprocessor.fit(cancer_train)
    scaled_cancer_train = cancer_preprocessor.transform(cancer_train)
    scaled_cancer_test = cancer_preprocessor.transform(cancer_test)

    scaled_cancer_train.to_csv(os.path.join(data_to, "scaled_cancer_train.csv"), index=False)
    scaled_cancer_test.to_csv(os.path.join(data_to, "scaled_cancer_test.csv"), index=False)

if __name__ == '__main__':
    main()