# wxm-synthetic-data

## Background

Sourced from:

-   Awesome synthetic data list: https://github.com/gretelai/awesome-synthetic-data?tab=readme-ov-file
-   SDV README: https://github.com/sdv-dev/SDV?tab=readme-ov-file
-   SDV docs: https://docs.sdv.dev/sdv/demos
-   SDV notebook demo: https://colab.research.google.com/drive/1MCTkTj9-93Ei-cLDQoj9AXaqPhpue7a3
-   For visualization (e.g., `metadata.visualize()`), install `graphviz` (https://graphviz.gitlab.io/download/)
-   Deps include `sdv` (for synthetic data generation) and `pandas` (for data manipulation) and `kaleido` (for plotly static image export) and `tabulate` (for pretty printing)

## Setup

```sh
# Install dependencies
pipenv shell
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

## Credits

This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
