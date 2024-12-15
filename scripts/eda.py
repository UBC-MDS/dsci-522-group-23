"""
python scripts/eda.py \
    --train-df-path='data/processed/train_df.csv' \
    --outdir='results/figures/eda/' \
"""

import altair as alt
import pandas as pd
import numpy as np
import click
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.plot_utils as eda 


@click.command()
@click.option("--train-df-path", type=str, help="relative path of the train DataFrame")
@click.option("--outdir", type=str, help="relative path of to save the EDA figures")
def plot_eda(train_df_path, outdir):

    """
    Generates and saves exploratory data analysis (EDA) figures, including a target distribution plot, 
    density plots for numerical variables, and a correlation matrix plot.

    Parameters
    ----------
    train_df_path : str
        Relative path to the training DataFrame CSV file.
    outdir : str
        Relative path to the directory where the EDA figures will be saved.

    Returns
    -------
    tuple
        A tuple containing the following:
        - `altair.Chart`: The Altair chart for the target distribution plot.
        - `matplotlib.figure.Figure`: The Matplotlib figure for density plots of numeric variables.
        - `altair.Chart`: The Altair chart for the correlation matrix plot.

    Examples
    --------
    To run this function via the command line:
    ```bash
    python scripts/eda.py \
        --train-df-path='data/processed/train_df.csv' \
        --outdir='results/figures/eda/'
    ```
    """

    train_df = pd.read_csv(train_df_path)
    os.makedirs(outdir, exist_ok=True)

    # distribution histogram
    xy_enc = {
        "x": ('G3:Q', 'Final Grades (G3)'),
        "y": ('count()', 'Number of Students')
    }
    props = {
        "title": 'Distribution of Final Grades (G3)',
        "width": 400,
        "height": 200
    }
    dist_plot = eda.distribution_plot(train_df=train_df,xy_enc=xy_enc, **props)
    saved_path = Path(outdir, "g3_dist.png")
    dist_plot.save(saved_path)
    print(f"Saved figure to {saved_path}")

    # variables density plots
    props = {"nrows": 3, "ncols": 3, "figsize": (8, 8), "sharey": False, "sharex": False}
    fig, axes = eda.density_plots(train_df=train_df, **props)
    saved_path =Path(outdir, "density_plots.png")
    fig.savefig(saved_path)
    print(f"Saved figure to {saved_path}")

    # correlation matrix plot
    props = {
        "width": 250,
        "height": 250,
        "title": "Pairwise correlations between variables (including target)"
    }
    corr_mat_chart = eda.pearson_corr_plot(train_df=train_df, **props)
    saved_path = Path(outdir, "corr_mat.png")
    corr_mat_chart.save(saved_path)
    print(f"Saved figure to {saved_path}")

    return (dist_plot, fig, corr_mat_chart)

if __name__ == "__main__":
    plot_eda()
    