# Contributing to our project

This outlines how to propose a change to this project. 

### Fixing typos

Small typos or grammatical errors in documentation may be edited directly using
the GitHub web interface, so long as the changes are made in the _source_ file.

*  `YES`: you edit `.py`, `.ipynb`, `.md` files.
*  `NO`: you edit an `.html` file, or any other files not listed in `YES`.

### Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and illustrate the bug with a minimal reproducible example (MRE).

A reproducible example should include the following:

- Clear Description: Explain what the issue or feature is.
- Minimal Code: Provide a minimal piece of code that demonstrates the problem or change.
- Expected Output: Specify what you expect the output to be.
- Actual Output: Describe what actually happens when you run the code.

Here's an example of a MRE

```python
# Example of a minimal code to demonstrate the issue/feature
import pandas as pd

# Create a simple DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Math': [90, 85, 92],
        'Science': [88, 79, 94]}

df = pd.DataFrame(data)

# Example operation that causes the issue
df['Average'] = df[['Math', 'Science']].mean(axis=1)

# Expected output: DataFrame with 'Average' column calculated
print(df)
```

What to include:

- Issue Example: If the code has a bug, describe the issue. For example, "The calculation for 'Average' is incorrect due to missing values."
- Expected Behavior: For example, "The 'Average' column should be computed correctly even with missing data."

### Pull request process

* Please create a Git branch for each pull request (PR).
* Provide a descriptive title for your PR and include any relevant information in the PR description:
  - What is the purpose of the change?
  - What issue does it address (if applicable)?
  - Any additional notes for the reviewers (e.g., tests added, documentation updated)
* New code should follow the [NumpyDoc style guide](https://numpydoc.readthedocs.io/en/latest/format.html#conclusion) or PEP8 [style guide](https://www.python.org/dev/peps/pep-0008/).

### Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.

### Attribution

These contributing guidelines were adapted from the [Breast Cancer Predictor Project contributing guidelines](https://github.com/ttimbers/breast_cancer_predictor_py/blob/main/CONTRIBUTING.md).