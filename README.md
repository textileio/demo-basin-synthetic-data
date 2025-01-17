# Basin Synthetic Data Demo

> Generate synthetic data for Basin datasets

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [Setup](#setup)
  - [Generate synthetic data](#generate-synthetic-data)
- [Contributing](#contributing)
- [License](#license)

## Background

This demo shows how to generate synthetic data derived from Basin storage. The data is generated using the Synthetic Data Vault (SDV) package, which is a Python library for generating synthetic data using a variety of models. The source data is weather data from WeatherXM's `wxm.weather_data_dev` vault, which has new weather data written to it on a daily basis.

Review the following files for the final results:

- [`diagnostic.md`](./diagnostic.md): A comparison of the original and synthetic data.
- [`plots`](./plots/): A directory containing plots of the original and synthetic data.
- [`synthetic_data.csv`](./synthetic_data.csv): The synthetic data generated by SDV.
- [`data.csv`](./data.csv): The original data from the WeatherXM vault.

For reference, this demo was sourced from the [Awesome Synthetic Data](https://github.com/gretelai/awesome-synthetic-data?tab=readme-ov-file) list and uses the following:

- SDV docs: [README](https://github.com/sdv-dev/SDV?tab=readme-ov-file), [site](https://docs.sdv.dev/sdv/demos), [notebook](https://colab.research.google.com/drive/1MCTkTj9-93Ei-cLDQoj9AXaqPhpue7a3)
- For visualizations (e.g., `metadata.visualize()`), install [`graphviz`](https://graphviz.gitlab.io/download/)
- Dependencies include `sdv` (for synthetic data generation), `pandas` (for data manipulation), `kaleido` (for plotly static image exports), and `tabulate` (for pretty printing to markdown).

## Install

First, set up the [`pipenv`](https://github.com/pypa/pipenv/) environment, install dependencies, and set up pre-commit and pre-push hooks:

```sh
# Install dependencies
pipenv shell
make install

# Setup pre-commit and pre-push hooks
make setup
```

## Usage

### Setup

You can use whatever data you'd like, but this demo uses CSV file is generated from the WeatherXM vault. To generate the CSV file, [download any event](https://basin.tableland.xyz/vaults/wxm.weather_data_dev/events) from the `wxm.weather_data_dev` vault and save it as `data.csv`. You can do this with a combination of `curl` and DuckDB. The DuckDB query below will take the downloaded parquet file, filter it so that only 10 records per device ID exist in the dataset, and also limit the sample to 10000 rows. Without this, it's possible all of the rows are the same device ID, which would lead to erroneous results.

```sh
> curl 'https://basin.tableland.xyz/events/bafybeid64vmetvduzsvmvisbn7ldgwruva6x7wm2pg2ty4jzqq4c4vmrm4' -o data.parquet
> duckdb
> COPY (SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY timestamp) as rn FROM read_parquet('data.parquet')) subquery WHERE rn <= 10 limit 10000) TO 'data.csv' (FORMAT 'csv');
```

A sample file is provided as `data.csv` in the root of this repository.

### Generate synthetic data

All that's left is to generate the synthetic data. The `synthetic_data/__main__.py` script will read the CSV file, generate a synthetic dataset, and save it as `synthetic_data.csv`. You can run the script with the following command:

```sh
make run
```

This will do a few things:

- Load the data from `data.csv` and generate synthetic data using SDV.
- Save the synthetic data to `synthetic_data.csv`.
- Run a diagnostic on the synthetic data to compare it to the original data and save this as `diagnostic.md`.
- Generate plots of the comparison and save them in the `plots` directory.

## Contributing

PRs accepted. Special thanks to Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.

Small note: If editing the README, please conform to the standard-readme specification.

## License

MIT AND Apache-2.0, © 2021-2024 Textile Contributors
