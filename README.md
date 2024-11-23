# Predicting Academic Performance in Mathematics using Demographic and Student Behavioral Data
## dsci-522-group-23

This is group#23 repository for DSCI 522 
- Author: Zhengling Jiang, Colombe Tolokin, Franklin Aryee, Tien Nguyen

In this project, we aim to address this question: “Can we predict a student's math academic performance based on the demographic and behavioral data?”. We will test out various machine learning algorithms and pick the best one that can reliably predict a student final grades base on the features.

## Collaborative Development Workflow Reminders:

### Branching

- Whenever you start working on a new feature or bug fix, create a new branch. This keeps your changes separate from the main codebase.
- **Please consult the team before force pushing anything on the `main` branch.** Ideally we should be working on feature branches at all times.

### Syncing Local/Remote

- Before working, please run `git pull` to update your local repo. If you have uncommited work, run `git stash` before `git pull`, then after pulling you can run `git stash pop`.

## Software Installation

### `conda` and `conda-lock`

We assume that you have installed the `conda` software and `conda-lock` packages on your machine. For instructions on how to install those softwares, please see:
- `conda`: [https://conda-forge.org/download/](https://conda-forge.org/download/)
- `conda-lock`: [https://github.com/conda/conda-lock](https://github.com/conda/conda-lock)

We provided both the conda `environment.yml` and conda-lock.yml` files. To install the neccessary packages, first make sure you are in the root directory of the project (`dsci-522-group-23`). We highly recommended installing with `conda-lock`, but both method will works just fine.

- With `conda`

```bash
conda env create -f environment.yml
```
Or 

```bash
conda create -n 522-project-env --file conda-lock.yml
```

- With `conda-lock`

```bash
conda-lock install -n 522-project-env
```

To activate / deactivate the environment:

```bash
conda activate 522-project-env
```

```bash
conda deactivate
```

To generate a new `conda-lock` file:

```bash
conda-lock -f environment.yml -p <os>
```

Where `<os>` are any of the following platform `['linux-64', 'osx-64', 'osx-arm64', 'win-64']`. Omitting the `-p` will generate a lockfile for all platforms.

## Dependencies

conda: Version 23.9.0 or higher
conda-lock: Version 2.5.7 or higher
jupyterlab: Version 4.3.1 or higher
nb_conda_kernels: Version 2.5.1 or higher
Python and packages listed in [environment.yml](https://github.com/UBC-MDS/dsci-522-group-23/blob/main/environment.yml)
