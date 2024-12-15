import pytest
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.plot_utils import distribution_plot, density_plots, pearson_corr_plot

def test_distribution_plot():
    mock_data = {
        'G3': [12, 14, 16, 12, 15, 14, 16, 15, 15],
    }
    train_df = pd.DataFrame(mock_data)

    xy_enc = {
        "x": ('G3', 'Final Grades (G3)'),
        "y": ('count()', 'Number of Students')
    }
    props = {
        "title": 'Distribution of Final Grades (G3)',
        "width": 400,
        "height": 200
    }

    dist_plot = distribution_plot(train_df=train_df, xy_enc=xy_enc, **props)

    assert isinstance(dist_plot, alt.Chart)
    json_obj = dist_plot.to_dict()
    # print(json.dumps(json_obj, indent=4))
    assert json_obj['mark']['type'] == 'bar'
    assert json_obj['encoding']['x']['field'] == 'G3'
    assert json_obj['encoding']['x']['title'] == 'Final Grades (G3)'
    assert json_obj['encoding']['y']['aggregate'] == 'count'
    assert json_obj['encoding']['y']['title'] == 'Number of Students'
    assert json_obj['title'] == props['title']
    assert json_obj['width'] == props['width']
    assert json_obj['height'] == props['height']
    with pytest.raises(TypeError) as exc_info:
        distribution_plot(train_df=[1,2,3], xy_enc=xy_enc, **props)
        distribution_plot(train_df=train_df, xy_enc=(0,1,2), **props)

def test_density_plots():
    mock_data = {
        'var1': np.random.randn(100),
        'var2': np.random.randn(100),
        'var3': np.random.randn(100),
        'var4': np.random.randn(100),
        'var5': np.random.randn(100),
        'var6': np.random.randn(100),
    }
    train_df = pd.DataFrame(mock_data)

    props = {
        "nrows": 2,
        "ncols": 3,
        "figsize": (12, 4),
        "sharey": True,
        "sharex": False
    }

    fig, axes = density_plots(train_df=train_df, **props)

    assert isinstance(fig, plt.Figure)
    assert tuple(plt.gcf().get_size_inches()) == props['figsize']
    assert axes.shape == (2,3)
    for ax in axes.flatten():
        assert isinstance(ax, plt.Axes)
        assert ax.has_data()  # Ensure each subplot has data
    with pytest.raises(TypeError) as exc_info:
        density_plots(train_df=[1,2,3], **props)

def test_pearson_corr_plot():
    
    mock_data_faulty = {
        'var1': np.random.randn(100),
        'var2': np.random.randn(100),
        'var3': np.random.randn(100),
        'target': np.random.randn(100)
    }
    faulty_df = pd.DataFrame(mock_data_faulty)
    mock_data = {
        'x1': np.random.randn(100),
        'x2': np.random.randn(100),
        'x3': np.random.randn(100),
        'target': np.random.randn(100)
    }
    train_df = pd.DataFrame(mock_data)

    props = {
        "width": 250,
        "height": 250,
        "title": "Pairwise correlations"
    }

    corr_mat_chart = pearson_corr_plot(train_df=train_df, **props)

    assert isinstance(corr_mat_chart, alt.Chart)
    json_obj = corr_mat_chart.to_dict()
    print(json.dumps(json_obj, indent=4))
    assert json_obj['mark']['type'] == 'circle'
    assert json_obj['encoding']['x']['field'] == 'var1'
    assert json_obj['encoding']['x']['title'] == 'variable 1'
    assert json_obj['encoding']['y']['field'] == 'var2'
    assert json_obj['encoding']['y']['title'] == 'variable 2'
    assert json_obj['encoding']['color']['field'] == 'correlation'
    assert json_obj['encoding']['color']['scale']["domain"] == [-1, 1]
    assert json_obj['encoding']['color']['scale']["scheme"] == "blueorange"
    assert json_obj['encoding']['size']['field'] == "abs_corr"
    assert json_obj['title'] == props['title']
    assert json_obj['width'] == props['width']
    assert json_obj['height'] == props['height']
    with pytest.raises(TypeError) as exc_info:
        pearson_corr_plot(train_df=[1,2,3], **props)
    with pytest.raises(ValueError) as exc_info:
        pearson_corr_plot(train_df=faulty_df, **props)


if __name__ == "__main__":
    test_distribution_plot()
    test_density_plots()
    test_pearson_corr_plot()
