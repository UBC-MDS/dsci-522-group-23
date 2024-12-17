# CHANGELOG

This file documents improvements made to the project in response to feedback from the DSCI 522 teaching team and peer reviews. 
Each change is linked to specific feedback and provides evidence of how the feedback was addressed.

---
## 1. Adding example usage screenshot
### Feedback:
It was suggested to include example usage screenshots to improve user experience.

### Changes Made:
Embedded the screenshot of example usage in the README.md file.
### Evidence:
commit: https://github.com/UBC-MDS/dsci-522-group-23/commit/10da7023edaf5fb57dc2e71f304a14059522f937

## 2. Define MSE, RMSE and MAE
### Feedback:
It was suggested to define the test statistics.
### Changes Made:
Add definitions of MSE, RMSE and MAE to the report.
### Evidence:
commit: https://github.com/UBC-MDS/dsci-522-group-23/commit/0d44281e06e953d1f0ca6bd2a40a111a1cbf7242

## 3. Spelling/Grammar Checks in report
### Feedback:
It was suggested to correct several spelling and grammatical mistakes throughout the report.
### Changes Made:
Corrected all identified spelling mistakes (e.g., "behaviour" to "behavior," "distirbution" to "distribution"). Revised sentences with grammatical issues for clarity and readability.
### Evidence:
git issue: https://github.com/UBC-MDS/dsci-522-group-23/issues/63#issue-2734901382


## 4. M1 feedback from teaching team: Versions are missing from environment files(s) for all Python packages
### Feedback:
Versions are missing from environment files(s) for all Python packages
### Changes Made:
Specify versions for all Python packages in the environment files.
### Evidence:
Check the environment.yml: https://github.com/UBC-MDS/dsci-522-group-23/blob/main/environment.yml 

## 5. M1 feedback from teaching team: Introduction issues
### Feedback:
- Target/response variable needs to be more clearly defined. 
- Did not clearly identify and describe the dataset that was used to answer the question.
### Changes Made:
The target variable has been clearly defined, and the dataset used to answer the question has been identified and described in detail within the Introduction section.
### Evidence:
Commit: https://github.com/UBC-MDS/dsci-522-group-23/commit/d06bd75d9236f7fa5e59c271ccf59bde1c43bca6

## 6. M2 feedback from teaching team: The platform key and value is missing from the docker-compose.yml file, 
### Feedback:
The platform key and value is missing from the  docker-compose.yml file, causing issues when running on different chip architectures.
### Changes Made:
Replaced `jupyter-notebook:` with `student-performance-predictor-env:` to ensure a more specific and appropriate service name.
### Evidence:
Commit: [https://github.com/UBC-MDS/dsci-522-group-23/commit/d06bd75d9236f7fa5e59c271ccf59bde1c43bca6](https://github.com/UBC-MDS/dsci-522-group-23/commit/008b657bfcfd1ed416e948bf9621d543d31d5805)

## 7. M2 feedback from teaching team: Reproducibility
### Feedback:
Could not reproducibly run the analysis because the computational environment cannot be recreated from the provided instructions and/or environment specification files.
### Changes Made:
We replaced the process of building the image locally with pulling the pre-built image directly from our DockerHub repository.
### Evidence:
Commit: [https://github.com/UBC-MDS/dsci-522-group-23/commit/d06bd75d9236f7fa5e59c271ccf59bde1c43bca6](https://github.com/UBC-MDS/dsci-522-group-23/commit/008b657bfcfd1ed416e948bf9621d543d31d5805)

## 8. Feedback from Peer Review: Results & Discussion Section
### Feedback:
The section lacked depth in explaining coefficients, model limitations, and the role of multicollinearity. Additionally, the justification for using Ridge Regression and discussion of results needed more clarity.
### Changes Made:
Expanded discussion on the model coefficients, explained the linearity assumption and provided examples, improved clarity on Ridge’s handling of multicollinearity through coefficient shrinkage and clarified why Ridge Regression was chosen.
### Evidence:
resolved git issue: https://github.com/UBC-MDS/dsci-522-group-23/issues/60
