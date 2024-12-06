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
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


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

    # target distribution plot
    dist_plot = alt.Chart(train_df).mark_bar().encode(
        x=alt.X('G3:Q', bin=True, title='Final Grades (G3)'),
        y=alt.Y('count()', title='Number of Students'),
        tooltip=['G3']
    ).properties(
        title='Distribution of Final Grades (G3)',
        width=400,
        height=200
    )
    saved_path = Path(outdir, "g3_dist.png")
    dist_plot.save(saved_path)
    print(f"Saved figure to {saved_path}")

    # variables density plots
    fig, axes = plt.subplots(3, 3, figsize=(8, 8), sharey=False, sharex=False)
    axes = axes.flatten()
    numeric_columns = train_df.select_dtypes(include='number').columns
    for i, column in enumerate(numeric_columns):
        dp = sns.kdeplot(data=train_df, x=column, fill=True, ax=axes[i])
    plt.tight_layout()
    saved_path =Path(outdir, "density_plots.png")
    plt.savefig(saved_path)
    print(f"Saved figure to {saved_path}")

    # correlation matrix plot
    corr_mat = train_df.select_dtypes(include='number').corr() \
        .reset_index(names="var1") \
        .melt(id_vars="var1", var_name="var2", value_name="correlation")
    # get rid of "duplicated" correlation
    corr_mat = corr_mat[corr_mat['var1'] <= corr_mat['var2']].reset_index(drop=True)
    corr_mat["abs_corr"] = np.abs(corr_mat["correlation"])
    corr_mat_chart = alt.Chart(corr_mat).mark_circle().encode(
        alt.X("var1").title("variable 1"),
        alt.Y("var2").title("variable 2"),
        alt.Color("correlation").scale(domain=[-1, 1], scheme="blueorange"),
        alt.Size("abs_corr").legend(None)
    ).properties(
        width=250,
        height=250,
        title="Pairwise correlations between variables (including target)"
    )
    saved_path = Path(outdir, "corr_mat.png")
    corr_mat_chart.save(saved_path)
    print(f"Saved figure to {saved_path}")

    return (dist_plot, fig, corr_mat_chart)

if __name__ == "__main__":
    plot_eda()
    