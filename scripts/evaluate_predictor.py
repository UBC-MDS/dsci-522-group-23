# evaluate_predictor.py

import click
import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

@click.command()
@click.option('--test_data', type=str, help="Path to test data")
@click.option('--predictions', type=str, help="Path to predictions")
@click.option('--best_model', type=str, help="Path to best_model")
@click.option('--metrics_to', type=str, help="Path to directory where metrics will be written")
@click.option('--coefs_to', type=str, help="Path to directory where coefficients will be written")
@click.option('--plot_to', type=str, help="Path to directory where plots will be written")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(test_data, predictions, best_model, metrics_to, coefs_to, plot_to, seed):
    """Evaluates the performance predictor on the test data 
    and saves the evaluation results."""
    np.random.seed(seed)
    
    # read the test data and predictions
    test_df = pd.read_csv(test_data)
    predictions_df = pd.read_csv(predictions)
    
    y_test = test_df['G3']
    y_pred = predictions_df['G3']

     # Calculate performance metrics
    mse = mean_squared_error(y_test, y_pred) # Mean squared error
    rmse = np.sqrt(mse) # Root Mean Squared error
    mae = mean_absolute_error(y_test, y_pred) # Mean Absolute Error

    # Create a DataFrame for metrics
    metrics_df = pd.DataFrame({
        "Metric": ["Mean Squared Error (MSE)", 
                   "Root Mean Squared Error (RMSE)", 
                   "Mean Absolute Error (MAE)"],
        "Value": [mse, rmse, mae]
    })
    
    metrics_df = metrics_df.set_index('Metric')
    
    metrics_df.to_csv(os.path.join(metrics_to, "evaluation_metrics.csv"), index=False)
    print(f"Metrics saved to {os.path.join(metrics_to, 'evaluation_metrics.csv')}")

    with open(best_model, 'rb') as f:
        best_model = pickle.load(f)
    
    # Extract and visualize coefficients
    coefs = best_model.named_steps['ridge'].coef_
    feature_names = best_model.named_steps['columntransformer'].get_feature_names_out().tolist()
    feature_names = [n.split("__")[1] for n in feature_names]

    # Create a DataFrame for coefficients
    coefs_df = pd.DataFrame({"features": feature_names, "coefs": coefs})
    
    # Save coefficients to a CSV file
    coefs_path = os.path.join(coefs_to, "ridge_coefficients.csv")
    coefs_df.to_csv(coefs_path, index=False)
    print(f"Coefficients saved to {coefs_path}")
    
    # Create a bar plot for coefficients
    plt.bar(feature_names, coefs)
    plt.xlabel("Features")
    plt.ylabel("Coefficient Value")
    plt.title("Ridge Regression Coefficients")
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(plot_to, "coefficients_plot.png"))
    print(f"Coefficient plot saved to {os.path.join(plot_to, 'coefficients_plot.png')}")
    
    
if __name__ == '__main__':
    main()
