# evaluate_predictor.py

"""
python scripts/evaluate_model.py \
    --y-test=data/processed/y_test.csv \
    --X-test=data/processed/X_test.csv \
    --best-model=results/models/best_model.pkl \
    --metrics-to=results/table/metrics/ \
    --coefs-to=results/table/coefficients/ \
    --plot-to=results/figures/
'"""

import click
import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error


@click.command()
@click.option('--y-test', type=str, required=True, help="Path to y test data")
@click.option('--X-test', 'X_test',type=str, required=True, help="Path to X test data")
@click.option('--best-model', type=str, required=True, help="Path to best model (pickle file)")
@click.option('--metrics-to', type=str, required=True, help="Path to directory where metrics will be saved")
@click.option('--coefs-to', type=str, required=True, help="Path to directory where coefficients will be saved")
@click.option('--plot-to', type=str, required=True, help="Path to directory where plots will be saved")
   
def main(y_test, X_test, best_model, metrics_to, coefs_to, plot_to):
    """
    Evaluates the performance predictor on the test data 
    and saves the evaluation results, including metrics table, coefficients table, and coefficients bar plot.
	
	Parameters
	----------
	y_test: str
		Path to the y test dataset.
	X_test: str
		Path to the X test dataset.
	best_model: str
		Path to the best model object.
	Metrics_to: str
		Path where the mertics table will be saved.
	Coefs_to: str
		Path where the coefficients table will be saved.
	Plot_to: str
		Path where the bar plot of coefficients will be saved.
		
	Returns
	-------
	 None
    	The function does not return any values but saves the following outputs to the specified paths:
	    - A CSV file containing evaluation metrics (saved to the path specified by `metrics_to`).
	    - A CSV file containing the coefficients table (saved to the path specified by `coefs_to`).
	    - A bar plot of coefficients in PNG format (saved to the path specified by `plot_to`).
	
	Examples
	--------
	To run this function via the command line: 
	```bash
	python scripts/evaluate_model.py \
    --y-test=data/processed/y_test.csv \
    --X-test=data/processed/X_test.csv \
    --best-model=results/models/best_model.pkl \
    --metrics-to=results/table/metrics/ \
    --coefs-to=results/table/coefficients/ \
    --plot-to=results/figures/
	 ```
"""
    
    # Ensure output directories exist
    os.makedirs(metrics_to, exist_ok=True)
    os.makedirs(coefs_to, exist_ok=True)
    os.makedirs(plot_to, exist_ok=True)
    
    # Load test data
    y_test = pd.read_csv(y_test)
    X_test = pd.read_csv(X_test)

    # Load the best model
    with open(best_model, 'rb') as f:
        best_model = pickle.load(f)
    
    # Make predictions
    y_pred = best_model.predict(X_test)

    # Calculate performance metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)

    # Save metrics
    metrics_df = pd.DataFrame({
        "Metric": ["Mean Squared Error (MSE)", 
                   "Root Mean Squared Error (RMSE)", 
                   "Mean Absolute Error (MAE)"],
        "Value": [mse, rmse, mae]
    })
    metrics_path = os.path.join(metrics_to, "evaluation_metrics.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"Metrics saved to {metrics_path}")
    
    # Extract and save coefficients
    coefs = best_model.named_steps['ridge'].coef_
    feature_names = best_model.named_steps['columntransformer'].get_feature_names_out().tolist()

    coefs_df = pd.DataFrame({"features": feature_names, "coefs": coefs})
    coefs_path = os.path.join(coefs_to, "ridge_coefficients.csv")
    coefs_df.to_csv(coefs_path, index=False)
    print(f"Coefficients saved to {coefs_path}")
    
    # Save bar plot of coefficients
    plt.figure(figsize=(10, 6))
    plt.bar(feature_names, coefs)
    plt.xlabel("Features")
    plt.ylabel("Coefficient Value")
    plt.title("Ridge Regression Coefficients")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plot_path = os.path.join(plot_to, "coefficients_plot.png")
    plt.savefig(plot_path)
    print(f"Coefficient plot saved to {plot_path}")


if __name__ == '__main__':
    main()
