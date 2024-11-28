# Predicting Academic Performance in Mathematics using Demographic and Student Behavioral Data

## dsci-522-group-23

### Author: Zhengling Jiang, Colombe Tolokin, Franklin Aryee, Tien Nguyen

## Summary

This project investigates whether a student's mathematics performance can be predicted with linear regression using demographic and behavioral data, aiming to help educators in supporting students and tailoring educational strategies.

## Usage

This section details the step to install the softwares and packages to run the analysis

### `conda` and `conda-lock`

We assume that you have installed the `conda` software and `conda-lock` packages on your machine. For instructions on how to install those softwares, please see:

- `conda`: [https://conda-forge.org/download/](https://conda-forge.org/download/)
- `conda-lock`: [https://github.com/conda/conda-lock](https://github.com/conda/conda-lock)

See the [Dependencies](#dependencies) section below to install the appropriate softare versions

### Clone the git repository from GitHub

In your terminal, please run the following commands:

```bash
git clone https://github.com/UBC-MDS/dsci-522-group-23.git
```

### Setup `conda` environment

We provided both the conda `environment.yml` and `conda-lock.yml` files. To install the neccessary packages, first make sure you are in the root directory of the project (`dsci-522-group-23`). We highly recommended installing with `conda-lock`, but both method will works just fine.

#### With `conda`

```bash
conda env create -f environment.yml
```

Or

```bash
conda create -n 522-project-env --file conda-lock.yml
```

#### With `conda-lock`

```bash
conda-lock install --name 522-project-env conda-lock.yml
```

Both method will create a new conda environment called `522-project-env` that contains the neccessary packages to run the analysis

#### To activate / deactivate the environment

```bash
conda activate 522-project-env
```

```bash
conda deactivate
```

#### Launch Jupyter Lab and run the analyses

1. Navigate to the root of this project on your computer and run the following command to create and start containers:

```bash
docker compose up
```
2. In the terminal, look for a URL: `http://127.0.0.1:8888/lab`. Copy and paste the URL into your browser and change `8888` to `8889` manually.

3. To run the analysis, open `notebooks/student_performance_predictor_report.ipynb` in the Jupyterlab that just launched and click "Restart Kernel and Run All Cells..." under the "Kernel" menu.

#### Clean Up
1. Shut Down the Container

To stop the container, press Ctrl + C in the terminal where you launched the container using docker compose up.

2. Remove the Container

Once the container is stopped, remove it and its associated resources by running:

```bash
docker compose rm
```

Navigate to the notebook file [student_performance_predictor_report.ipynb](notebooks/student_performance_predictor_report.ipynb) to view or rerun the analysis as you wish.

## Dependencies

- `conda`: Version 23.9.0 or higher

- `conda-lock`: Version 2.5.7 or higher

- Python and packages listed in [environment.yml](environment.yml) or [conda-lock.yml](conda-lock.yml)

## License

The project follows a dual licensing structure:

- The project code is licensed under the [MIT License](https://opensource.org/license/MIT). See the [LICENSE.md](https://github.com/UBC-MDS/dsci-522-group-23/blob/main/LICENSE.md) file for details.
- The project report is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license](https://creativecommons.org/licenses/by-nc-nd/4.0/).

If re-using or re-mixing this project, please ensure proper attribution and adherence to the terms of the respective licenses.

## Contributing

Please see the [Contributing Guidelines](CONTRIBUTING.md) for proper procedures to contribute to our project.
