from pathlib import Path

from pandas import DataFrame, read_csv
from sdmetrics.reports.single_table import DiagnosticReport, QualityReport
from sdv.evaluation.single_table import (
    evaluate_quality,
    get_column_plot,
    run_diagnostic,
)
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer


def get_origin_data(path: Path) -> tuple[DataFrame, SingleTableMetadata]:
    """
    Read the real data from a CSV file and generate metadata from it.

    Args:
        path (Path): The path to the CSV file.

    Returns:
        tuple[DataFrame, SingleTableMetadata]: The real data and metadata.
    """
    real_data = read_csv(path)
    # remove any rows with null column values
    real_data = real_data.dropna()
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(real_data)

    return real_data, metadata


def generate_synthetic_data(
    real_data: DataFrame, metadata: SingleTableMetadata
) -> DataFrame:
    """
    Generate synthetic data from the real data.

    Args:
        real_data (DataFrame): The real data.
        metadata (SingleTableMetadata): The metadata.

    Returns:
        DataFrame: The synthetic data.

    """
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(real_data)
    synthetic_data = synthesizer.sample(len(real_data))

    return synthetic_data


def analyze_data(
    real_data: DataFrame, synthetic_data: DataFrame, metadata: SingleTableMetadata
) -> tuple[DiagnosticReport, QualityReport]:
    """
    Analyze the synthetic data and compare it to the real data.

    Args:
        real_data (DataFrame): The real data.
        synthetic_data (DataFrame): The synthetic data.
        metadata (SingleTableMetadata): The metadata.

    Returns:
        tuple[DiagnosticReport, QualityReport]: The diagnostic and quality reports.
    """
    diagnostic = run_diagnostic(
        real_data=real_data,
        synthetic_data=synthetic_data,
        metadata=metadata,
        verbose=False,
    )
    quality_report = evaluate_quality(
        real_data, synthetic_data, metadata, verbose=False
    )

    return diagnostic, quality_report


def write_report(
    root: Path,
    diagnostic: DiagnosticReport,
    quality_report: QualityReport,
    synthetic_data: DataFrame,
):
    """
    Write the diagnostic and quality reports to a markdown file.

    Args:
        root (Path): The root directory to write the report to.
        diagnostic (DiagnosticReport): The diagnostic report.
        quality_report (QualityReport): The quality report.
        synthetic_data (DataFrame): The synthetic data.
    """
    with open(root / "diagnostic.md", "w") as f:
        f.write("# Diagnostic & Quality Report")
        f.write("\n\n")
        f.write("## Scores")
        f.write("\n\n")
        f.write("### Diagnostic")
        f.write("\n\n")
        d_score = diagnostic.get_score()
        f.write("Overall score: " + "{:,.2%}".format(d_score))
        f.write("\n\n")
        d_props = diagnostic.get_properties()
        f.write(d_props.to_markdown())
        f.write("\n\n")
        f.write("### Quality")
        f.write("\n\n")
        q_score = quality_report.get_score()
        f.write("Overall score: " + "{:,.2%}".format(q_score))
        f.write("\n\n")
        q_props = quality_report.get_properties()
        f.write(q_props.to_markdown())
        f.write("\n\n")
        f.write("By column: ")
        f.write("\n\n")
        col_shapes = quality_report.get_details("Column Shapes")
        f.write(col_shapes.to_markdown())
        f.write("\n\n")
        f.write("## Sample synthetic data")
        f.write("\n\n")
        f.write(synthetic_data.head(10).to_markdown())
        # Write links to the plots
        f.write("\n\n")
        f.write("## Plots")
        f.write("\n\n")
        f.write("### Column plots")
        f.write("\n\n")
        for column in synthetic_data.columns:
            f.write(f"![{column}](plots/{column}_plot.png)")
            f.write("\n\n")


def plot_analysis(
    root: Path,
    real_data: DataFrame,
    synthetic_data: DataFrame,
    metadata: SingleTableMetadata,
):
    """
    Generate plots for the real and synthetic data.

    Args:
        root (Path): The root directory to write the plots to.
        real_data (DataFrame): The real data.
        synthetic_data (DataFrame): The synthetic data.
        metadata (SingleTableMetadata): The metadata.
    """
    columns = [
        "device_id",
        "timestamp",
        "temperature",
        "humidity",
        "precipitation_accumulated",
        "wind_speed",
        "wind_gust",
        "wind_direction",
        "illuminance",
        "solar_irradiance",
        "fo_uv",
        "uv_index",
        "precipitation_rate",
        "pressure",
        "name",
        "utc_datetime",
        "model",
        "cell_id",
        "lat",
        "lon",
        "rn",
    ]
    for column in columns:
        fig = get_column_plot(
            real_data=real_data,
            synthetic_data=synthetic_data,
            column_name=column,
            metadata=metadata,
        )

        fig.to_image(format="png")
        path = root / "plots" / f"{column}_plot.png"
        fig.write_image(path)
