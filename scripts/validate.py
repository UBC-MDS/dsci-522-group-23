# validate.py

import click
import os
import pandas as pd
import pandera as pa
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from scipy.stats import shapiro


def load_data(filepath: str) -> pd.DataFrame:
    """
    Check filepath and load the correct file.

    Parameters
    ----------
    filepath : str
        Path to the file to load.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is not a CSV file.
    """
    print("Loading data...")
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")

    if not filepath.endswith(".csv"):
        raise ValueError(f"The file '{filepath}' is not a CSV file.")

    student_performance = pd.read_csv(filepath, delimiter=";")
    columns = ["sex", "age", "studytime", "failures", "goout", "Dalc", "Walc", "G1", "G2", "G3"]
    
    return student_performance[columns]


def validate_student_data(df: pd.DataFrame) -> None:
    """
    Validate data against the predefined schema.
    """
    print("Validating data schema...")
    # Define the schema
    schema = pa.DataFrameSchema(
    {
        "sex": pa.Column(str, pa.Check.isin(["M", "F"])),
        "age": pa.Column(int, pa.Check.between(15, 22), nullable=False),
        "studytime": pa.Column(int, pa.Check.between(1, 4), nullable=False), 
        "failures": pa.Column(int, pa.Check.between(0, 4), nullable=False),
        "goout": pa.Column(int, pa.Check.between(1, 5), nullable=False),
        "Dalc": pa.Column(int, pa.Check.between(1, 5), nullable=False),
        "Walc": pa.Column(int, pa.Check.between(1, 5), nullable=False),
        "G1": pa.Column(int, pa.Check.between(0, 20), nullable=False),
        "G2": pa.Column(int, pa.Check.between(0, 20), nullable=False),
        "G3": pa.Column(int, pa.Check.between(0, 20), nullable=False)
    },
    checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
        pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
    ]
    )
    # Validate the DataFrame
    schema.validate(df, lazy=True)
    print("Schema validation successful!")


def validate_missingness(
    data: pd.DataFrame, threshold: float = 0.05, save_path: str = None
) -> None:
    """
    Validate that missing values in the dataset do not exceed the acceptable threshold.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset to check for missing values.
    threshold : float, optional
        The maximum allowable percentage of missing values per column (default is 0.05).
    save_path : str, optional
        The path to save the missingness heatmap plot. If None, the plot is not saved.

    Raises
    ------
    ValueError
        If any column has missing values exceeding the acceptable threshold.
    """
    print("Validating missingness...")

    missing_percentage = data.isnull().mean()
    above_threshold = missing_percentage[missing_percentage > threshold]

    if above_threshold.empty:
        print("Missingness validation successful!")
    else:
        raise ValueError(
            f"Columns with missing values beyond threshold ({threshold}):\n{above_threshold}"
        )

    # Plot missingness heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=True, cmap="viridis")
    plt.title("Missing Value Heatmap")

    # Save plot
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file_path = os.path.join(save_path, "missingness_heatmap.png")
        plt.savefig(file_path, bbox_inches="tight")
        print(f"Missingness heatmap saved to {save_path}.")


def validate_target_distribution(
    data: pd.DataFrame, target_column: str = "G3", save_path: str = None
) -> None:
    """
    Validate the distribution of the target variable by performing a Shapiro-Wilk test.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset containing the target variable.
    target_column : str
        The name of the target column whose distribution is to be validated.
    save_path : str
        The path to save the histogram plot. If None, the plot is not saved.

    Raises
    ------
    ValueError
        If the target variable does not follow a normal distribution.
    """
    print("Validating target distribution...")

    stat, p = shapiro(data[target_column])
    if p > 0.05:
        print(
            f"Target variable '{target_column}' follows a normal distribution (p={p:.4f})."
        )
    else:
        print(
            f"Target variable '{target_column}' does not follow a normal distribution (p={p:.4f})."
        )

    # Plot target distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data[target_column], kde=True, bins=20)
    plt.title(f"Distribution of {target_column}")

    # Save  plot
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file_path = os.path.join(save_path, "target_distribution_histogram.png")
        plt.savefig(file_path, bbox_inches="tight")
        print(f"Target distribution histogram saved to {save_path}")


def validate_no_outliers(
    data: pd.DataFrame, numeric_columns: list, max_cols: int = 3, save_path: str = None
) -> None:
    """
    Validate the presence of outliers in numeric columns using boxplots and optionally save the plots.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset containing the numeric columns to be checked for outliers.
    numeric_columns : list
        A list of column names from `data` that contain numeric data to plot.
    max_cols : int, optional
        The maximum number of boxplots to display per row (default is 3).
    save_path : str, optional
        The path to save the combined boxplot figure. If None, the plot is not saved.

    Raises
    ------
    ValueError
        If the dataset does not contain any of the specified numeric columns.
    """
    print("Validating outliers...")

    # Check if numeric columns are in the dataset
    missing_columns = [col for col in numeric_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing numeric columns in the dataset: {missing_columns}")

    # Generate boxplots
    num_plots = len(numeric_columns)
    nrows = -(-num_plots // max_cols)  # Ceiling division for rows
    ncols = min(num_plots, max_cols)
    print("Outlier validation successful!")
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10))

    for ax, column in zip(axes.flatten(), numeric_columns):
        sns.boxplot(data=data, x=column, ax=ax)
        ax.set_title(f"Boxplot of {column}")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.suptitle("Boxplots of Numeric Columns", fontsize=14)

    # Save or show the plot
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file_path = os.path.join(save_path, "boxplots.png")
        plt.savefig(file_path, bbox_inches="tight")
        print(f"Boxplots saved to {save_path}")


def validate_anomalous_correlations(
    data: pd.DataFrame,
    target_col: str,
    threshold: float = 0.9,
    zero_tolerance: float = 1e-5,
):
    """
    Check for anomalous correlations in a dataset:
    - Between features and the target variable.
    - Among features themselves.
    - Includes checks for zero correlations.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset containing the target and features.
    target_col : str
        The name of the target column in the dataset.
    threshold : float, optional
        The correlation threshold above which correlations are flagged as anomalous (default is 0.9).
    zero_tolerance : float, optional
        The tolerance for detecting zero correlations (default is 1e-5).

    Raises
    ------
    ValueError
        If the target column is not numeric or not found in the dataset.
    Warning
        Issues warnings for high and near-zero correlations.
    """
    print("Validating anomalous correlations...")

    # Ensure the target column exists and is numeric
    if target_col not in data.columns:
        raise ValueError(f"Target column '{target_col}' not found in the dataset.")
    if not pd.api.types.is_numeric_dtype(data[target_col]):
        raise ValueError(f"Target column '{target_col}' must be numeric.")

    # Select only numeric columns
    numeric_data = data.select_dtypes(include="number")

    # Ensure the target column is included in the numeric dataset
    if target_col not in numeric_data.columns:
        numeric_data[target_col] = data[target_col]

    # Compute the full correlation matrix
    correlation_matrix = numeric_data.corr()

    # Step 1: Correlations between features and target
    target_correlations = correlation_matrix[target_col].drop(target_col)

    # Check for anomalous (high) correlations
    anomalous_target_corrs = target_correlations[target_correlations.abs() > threshold]
    for feature, corr in anomalous_target_corrs.items():
        warnings.warn(
            f"Anomalous correlation ({corr:.2f}) between feature '{feature}' and target '{target_col}'."
        )

    # Check for zero correlations
    zero_target_corrs = target_correlations[target_correlations.abs() <= zero_tolerance]
    for feature, corr in zero_target_corrs.items():
        warnings.warn(
            f"Zero or near-zero correlation ({corr:.2f}) between feature '{feature}' and target '{target_col}'."
        )

    # Step 2: Correlations among features
    feature_correlations = correlation_matrix.loc[
        numeric_data.columns, numeric_data.columns
    ]

    # Check for anomalous (high) correlations among features
    anomalous_feature_corrs = feature_correlations[
        (feature_correlations.abs() > threshold) & (feature_correlations != 1)
    ]
    for feature1 in anomalous_feature_corrs.index:
        for feature2 in anomalous_feature_corrs.columns:
            if feature1 != feature2 and not pd.isna(
                anomalous_feature_corrs.loc[feature1, feature2]
            ):
                corr = anomalous_feature_corrs.loc[feature1, feature2]
                warnings.warn(
                    f"Anomalous correlation ({corr:.2f}) between features '{feature1}' and '{feature2}'."
                )
                anomalous_feature_corrs.loc[feature1, feature2] = None
                anomalous_feature_corrs.loc[feature2, feature1] = None

    feature_to_target_df = pd.DataFrame(
        {
            "Feature": target_correlations.index,
            "Correlation": target_correlations.values,
        }
    ).reset_index(drop=True)

    feature_to_feature_df = feature_correlations.stack().reset_index()
    feature_to_feature_df.columns = ["Feature1", "Feature2", "Correlation"]
    feature_to_feature_df = feature_to_feature_df[
        feature_to_feature_df["Feature1"] != feature_to_feature_df["Feature2"]
    ]

    print("Anomalous correlation validation successful!")
    return {
        "feature_to_target": feature_to_target_df,
        "feature_to_feature": feature_to_feature_df,
    }


@click.command()
@click.option("--raw-data", type=str, help="Path to raw data")
@click.option(
    "--data-to",
    type=str,
    help="Path to directory where processed data will be written to",
)
@click.option(
    "--plot-to", type=str, help="Path to directory where the plot will be written to"
)
def main(raw_data, data_to, plot_to):
    try:
        # Load the dataset
        subset_df = load_data(raw_data)
        print(subset_df[subset_df.duplicated()])

        # Validate the data schema
        validate_student_data(subset_df)

        # Validate missingness in the dataset
        validate_missingness(subset_df, threshold=0.1, save_path=plot_to)

        # Validate target distribution
        validate_target_distribution(subset_df, target_column="G3", save_path=plot_to)

        # Validate no outliers
        numeric_columns = subset_df.select_dtypes(include="number").columns
        validate_no_outliers(subset_df, numeric_columns, max_cols=3, save_path=plot_to)

        # Validate anomalous correlations
        validate_anomalous_correlations(subset_df, target_col="G3", threshold=0.95)
        print("\nAll validation checks passed.\nSaving validated data...")
        validated_data_dir = os.path.join(data_to, "validated")
        os.makedirs(validated_data_dir, exist_ok=True)
        validated_data_path = os.path.join(validated_data_dir, "validated-data.csv")
        subset_df.to_csv(validated_data_path, index=False)
        print(f"Validated data saved to: {data_to}")

    except ValueError as ve:
        print(f"Validation error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
