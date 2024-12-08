# fit_model.py

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--model-to', type=str, help="Path to directory where the best model will be saved")
@click.option('--test-data-to', type=str, help="Path to directory where test data (X_test, y_test) will be saved")
@click.option('--plot-to', type=str, help="Path to directory where the plots and tables will be written")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(training_data, pipeline_to, model_to, test_data_to, plot_to, seed):
    """
    Fits a student performance regression model to the training data, tunes its hyperparameters, and saves the results.

    The function performs the following tasks:
    1. Reads the training data and splits it into training and test sets.
    2. Benchmarks a baseline model using `DummyRegressor`.
    3. Preprocesses the data using scaling and encoding.
    4. Creates and tunes a Ridge regression model using grid search and cross-validation.
    5. Saves the trained pipeline, best model, test data, and evaluation plots to specified directories.

    Parameters
    ----------
    training_data : str
        Path to the CSV file containing the training data.
    pipeline_to : str
        Path to the directory where the trained pipeline object will be saved.
    model_to : str
        Path to the directory where the best model will be saved as a pickle file.
    test_data_to : str
        Path to the directory where test data (X_test, y_test) will be saved.
    plot_to : str
        Path to the directory where the plots and tables will be saved.
    seed : int
        Random seed for reproducibility. Defaults to 123.

    Returns
    -------
    None
        The function saves the trained pipeline, best model, test data, performance metrics, plots, and tables.

    Examples
    --------
    To execute this script via the command line, run the following command:

    ```bash
    python scripts/fit_model.py \
        --training-data=data/processed/train_df.csv \
        --pipeline-to=results/models/ \
        --model-to=results/models/ \
        --test-data-to=data/processed/test/ \
        --plot-to=results/plots/ \
        --seed=42
    ```
    """
    np.random.seed(seed)

    # Read in data
    student_train = pd.read_csv(training_data)
    X = student_train.drop(columns=["G3"])
    y = student_train["G3"]

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

    # Save test data for evaluation
    os.makedirs(test_data_to, exist_ok=True)
    X_test.to_csv(os.path.join(test_data_to, "X_test.csv"), index=False)
    y_test.to_csv(os.path.join(test_data_to, "y_test.csv"), index=False)
    print(f"Test data saved to {test_data_to}")

    # Baseline model (Dummy Regressor)
    dr = DummyRegressor(strategy="mean")
    dummy_cv = cross_validate(dr, X_train, y_train, return_train_score=True, cv=5)
    dummy_results = pd.DataFrame(dummy_cv).agg(['mean']).T
    print("Baseline Model Performance (Dummy Regressor):")
    print(dummy_results)

    # Save baseline results to a CSV file
    os.makedirs(plot_to, exist_ok=True)
    baseline_results_path = os.path.join(plot_to, "baseline_results.csv")
    dummy_results.to_csv(baseline_results_path)
    print(f"Baseline results saved to {baseline_results_path}")

    # Preprocessing pipeline
    categorical_feats = X_train.select_dtypes(include=['object']).columns
    numeric_feats = X_train.select_dtypes(include=['int64', 'float64']).columns

    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(drop="if_binary", sparse_output=False), categorical_feats),
        verbose_feature_names_out=False
    )

    # Ridge regression model
    pipe_lr = make_pipeline(preprocessor, Ridge(random_state=seed))

    # Hyperparameter tuning grid
    param_grid = {
        'ridge__alpha': [0.1, 1, 10, 100]
    }

    grid_search = GridSearchCV(
        pipe_lr,
        param_grid=param_grid,
        scoring="neg_mean_squared_error",
        cv=5,
        return_train_score=True
    )

    grid_search.fit(X_train, y_train)

    # Save best model
    os.makedirs(model_to, exist_ok=True)
    best_model_path = os.path.join(model_to, "best_model.pkl")
    with open(best_model_path, 'wb') as f:
        pickle.dump(grid_search.best_estimator_, f)
    print(f"Best model saved to {best_model_path}")

    # Save pipeline
    os.makedirs(pipeline_to, exist_ok=True)
    pipeline_path = os.path.join(pipeline_to, "student_pipeline.pkl")
    with open(pipeline_path, 'wb') as f:
        pickle.dump(grid_search, f)
    print(f"Pipeline saved to {pipeline_path}")

    # Grid search results
    grid_results = pd.DataFrame(grid_search.cv_results_)[
        [
            "mean_test_score",
            "param_ridge__alpha",
            "mean_fit_time",
            "rank_test_score",
        ]
    ].set_index("rank_test_score").sort_index()
    print("Hyperparameter Tuning Results:")
    print(grid_results)

    # Save grid search results to a CSV file
    grid_results_path = os.path.join(plot_to, "grid_search_results.csv")
    grid_results.to_csv(grid_results_path)
    print(f"Grid search results saved to {grid_results_path}")

    # Ridge regression coefficients
    feature_names = grid_search.best_estimator_.named_steps['columntransformer'].get_feature_names_out()
    coefficients = grid_search.best_estimator_.named_steps['ridge'].coef_

    coefs_df = pd.DataFrame({"Features": feature_names, "Coefficients": coefficients}).sort_values(by="Coefficients")

    # Save coefficients to a CSV file
    coefficients_path = os.path.join(plot_to, "ridge_coefficients.csv")
    coefs_df.to_csv(coefficients_path, index=False)
    print(f"Coefficients saved to {coefficients_path}")

    # Bar plot of coefficients
    plt.figure(figsize=(10, 6))
    plt.bar(coefs_df["Features"], coefs_df["Coefficients"])
    plt.xlabel("Features")
    plt.ylabel("Coefficient Value")
    plt.title("Ridge Regression Coefficients")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    coefficients_plot_path = os.path.join(plot_to, "ridge_coefficients.png")
    plt.savefig(coefficients_plot_path)
    plt.close()
    print(f"Coefficient plot saved to {coefficients_plot_path}")


if __name__ == '__main__':
    main()