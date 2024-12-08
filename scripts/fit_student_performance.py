# fit_student_performance.py
# author: dsci_522_group_23
# date: 2024-12-05

----
from deepchecks.tabular.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation
from deepchecks.tabular import Dataset
from sklearn import set_config
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import fbeta_score, make_scorer
from joblib import dump
import pandas as pd
----
import altair as alt
# import altair_ally as ally
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandera as pa
from scipy.stats import shapiro
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import cross_validate
alt.renderers.enable("mimetype")
%matplotlib inline

import click
import pickle

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="deepchecks")


@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--preprocessor', type=str, help="Path to preprocessor object")
@click.option('--columns-to-drop', type=str, help="Optional: columns to drop")
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--seed', type=int, help="Random seed", default=123

def main(training_data, preprocessor, columns_to_drop, pipeline_to, plot_to, seed):
    '''Fits a steudent performance regressor to the training data
    and saves the pipeline object'''
    
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data and preprocessor
    train_df = pd.read_csv(training_data)
    preprocessor = pickle.load(open(pre))
    






    