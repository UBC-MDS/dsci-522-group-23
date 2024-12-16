.PHONY: all clean tests

all: tests notebooks/report.html notebooks/report.pdf

PYTHON_TEST_FILES := $(wildcard tests/*.py)
tests: $(PYTHON_TEST_FILES)
	pytest $(PYTHON_TEST_FILES)

# Download and extract data
data/raw/student-mat.csv : scripts/download_data.py
	python scripts/download_data.py \
    	--url='https://archive.ics.uci.edu/static/public/320/student+performance.zip' \
    	--out-dir='data/raw' \
    	--raw-filename='student-mat.csv'

# Split and preprocess data
results/models/preprocessor.pickle data/processed/train_df.csv data/processed/test_df.csv data/processed/X_train.csv data/processed/y_train.csv data/processed/X_test.csv data/processed/y_test.csv : scripts/split_preprocess.py data/raw/student-mat.csv
	python scripts/split_preprocess.py \
		--raw-data='data/raw/student-mat.csv' \
		--data-to='data/processed/' \
		--preprocessor-to='results/models/'

# Validate data and save plots
results/figures/validate/ : scripts/validate.py data/raw/student-mat.csv
	python scripts/validate.py \
		--raw-data='data/raw/student-mat.csv' \
		--plot-to='results/figures/validate/'

# Perform EDA and save plots
results/figures/eda/ : scripts/eda.py data/processed/train_df.csv
	python scripts/eda.py \
		--train-df-path='data/processed/train_df.csv' \
		--outdir='results/figures/eda/'
	
# Train model, save pipeline and model
results/models/best_model.pkl results/plots/ data/processed/test/X_test.csv data/processed/test/y_test.csv : scripts/fit_model.py data/processed/train_df.csv
	python scripts/fit_model.py \
		--training-data=data/processed/train_df.csv \
		--pipeline-to=results/models/ \
		--model-to=results/models/ \
		--test-data-to=data/processed/test/ \
		--plot-to=results/plots/ \
		--seed=17
# Evaluate model and save results
results/table/metrics/ results/table/coefficients/ results/figures/coefficients_plot.png : scripts/evaluate_model.py data/processed/X_test.csv data/processed/y_test.csv results/models/best_model.pkl
	python scripts/evaluate_model.py \
		--y-test=data/processed/y_test.csv \
		--X-test=data/processed/X_test.csv \
		--best-model=results/models/best_model.pkl \
		--metrics-to=results/table/metrics/ \
		--coefs-to=results/table/coefficients/ \
		--plot-to=results/figures/
	
# Build HTML and PDF report
notebooks/report.html notebooks/report.pdf : notebooks/report.qmd \
notebooks/references.bib \
data/raw/student-mat.csv \
data/processed/train_df.csv \
results/models/best_model.pkl \
results/plots \
results/figures/eda/ \
results/figures/validate/ \
results/figures/coefficients_plot.png \
results/table/metrics/ \
results/table/coefficients/
	quarto render notebooks/report.qmd --to html
	quarto render notebooks/report.qmd --to pdf

# Clean up analysis
clean:
	rm -rf data/raw/*
	rm -rf data/processed/*
	rm -rf results/models/*
	rm -rf results/figures/*
	rm -rf results/plots/*
	rm -rf results/table/*
	rm -rf notebooks/report.html
	rm -rf notebooks/report.pdf
