"""
This module contains various plotting utility functions for convenience
"""

import altair as alt
import pandas as pd
import numpy as np
import click
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def distribution_plot(train_df: pd.DataFrame, xy_enc: dict, **kwargs) -> alt.Chart:
    """
    Creates a distribution histogram plot for a specified variable.

    Parameters
    ----------
    train_df : pandas.DataFrame
        The dataset containing the data to be plotted.
    xy_enc : dict
        A dictionary specifying the x-axis and y-axis encoding. Expected keys:
        - "x": tuple of str, str
            A tuple containing the column name for the x-axis and its label.
        - "y": tuple of str, str
            A tuple containing the aggregation function for the y-axis and its label.
    **props : dict
        Additional keyword arguments for customizing the plot, such as title, width, and height.

    Returns
    -------
    dist_plot : altair.Chart
        An Altair chart object representing the distribution histogram.
    """
    if not isinstance(train_df, pd.DataFrame):
        raise TypeError("train_df is not a pd.DataFrame object")
    if not isinstance(xy_enc, dict):
        raise TypeError("xy_enc is not a Dictionary object")
    dist_plot = alt.Chart(train_df).mark_bar().encode(
        x=alt.X(xy_enc['x'][0], bin=True, title=xy_enc['x'][1]),
        y=alt.Y(xy_enc['y'][0], title=xy_enc['y'][1]),
        tooltip=[xy_enc['x'][0]]
    ).properties(
        **kwargs
    )
    
    return dist_plot

def density_plots(train_df: pd.DataFrame, **kwargs) -> tuple:
    """
    Generates density plots for multiple variables in a grid layout.

    Parameters
    ----------
    train_df : pandas.DataFrame
        The dataset containing the data to be plotted.
    **props : dict
        Additional keyword arguments for customizing the plt.subplots() function

    Returns
    -------
    fig : matplotlib.figure.Figure
        The Matplotlib figure object containing the density plots.
    axes : numpy.ndarray
        A 2D array of Matplotlib axes objects for the subplots.
    """
    if not isinstance(train_df, pd.DataFrame):
        raise TypeError("train_df is not a pd.DataFrame object")
    fig, axes = plt.subplots(**kwargs)
    axes_flat = axes.flatten()
    numeric_columns = train_df.select_dtypes(include='number').columns
    for i, column in enumerate(numeric_columns):
        dp = sns.kdeplot(data=train_df, x=column, fill=True, ax=axes_flat[i])
    plt.tight_layout()
    
    return (fig, axes)

def pearson_corr_plot(train_df: pd.DataFrame, **kwargs) -> alt.Chart:
    
    """
    Creates a correlation matrix plot showing pairwise Pearson correlations.

    Parameters
    ----------
    train_df : pandas.DataFrame
        The dataset containing the data to be analyzed.
    **props : dict
        Additional keyword arguments for customizing the plot. Supported keys include:

    Returns
    -------
    plot : altair.Chart
        An Altair chart object representing the correlation matrix plot.

    Notes
    ------
    - The DataFrame should NOT contain any columns name "var1" and "var2", these are 
    reserved names for the implementation to work.
    """
    if not isinstance(train_df, pd.DataFrame):
        raise TypeError("train_df is not a pd.DataFrame object")
    if "var1" in train_df.columns or "var2" in train_df.columns:
        raise ValueError("Reserved names 'var1' or 'var2' exist. Please rename those columns")
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
       **kwargs
    )
    return corr_mat_chart