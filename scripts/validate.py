# validate.py

import click
import os


@click.command()
@click.option('--val-data', type=str, help="Path to validated data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")

def load_data(filepath: str) -> pd.DataFrame:
    ''''
    Check filepath and load correct file
    ''''
    if os.path.isfile(filepath):
        if filepath[-4:] == '.csv':
            df = pd.read_csv(filepath, delimiter=';')
            return df
    return "File is not in directory"


def validate_student_data(df: pd.DataFrame) -> None:
    '''
    Validate data against the predefined schema.
    '''
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
            "G3": pa.Column(int, pa.Check.between(0, 20), nullable=False)
        },
        checks=[
            pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ]
    )

    # Validate the DataFrame
    return schema.validate(df, lazy=True)


def validate_missingness(data: pd.DataFrame, threshold: float = 0.05, save_path: str = None) -> None:
    '''
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
    '''
    print("Validating missingness...")
    missing_percentage = data.isnull().mean()
    above_threshold = missing_percentage[missing_percentage > threshold]

    if above_threshold.empty:
        print("Missingness validation successful!")
    else:
        raise ValueError(f"Columns with missing values beyond threshold ({threshold}):\n{above_threshold}")

    # Plot missingness heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=True, cmap="viridis")
    plt.title("Missing Value Heatmap")
    
    # Save plot
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Missingness heatmap saved to {save_path}.")


def validate_target_distribution(data: pd.DataFrame, target_column: str = "G3", save_path: str = None) -> None:
    '''
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
    '''
    print("Validating target distribution...")
    stat, p = shapiro(data[target_column])
    if p > 0.05:
        print("Target distribution validation successful!")
    else:
        raise ValueError(f"Target variable '{target_column}' does not follow a normal distribution (p={p:.4f}).")
        
    # Plot target distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data[target_column], kde=True, bins=20)
    plt.title(f"Distribution of {target_column}")

    # Save  plot
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Target distribution histogram saved to {save_path}.")


def validate_no_outliers(data: pd.DataFrame, numeric_columns: list, max_cols: int = 3, save_path: str = None) -> None:
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

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10))

    for ax, column in zip(axes.flatten(), numeric_columns):
        sns.boxplot(data=subset_df, x=column, ax=ax)
        ax.set_title(f"Boxplot of {column}")
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.suptitle("Boxplots of Numeric Columns", fontsize=14)

    # Save or show the plot
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Boxplots saved to {save_path}.")