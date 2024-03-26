from pathlib import Path

from .run import (
    analyze_data,
    generate_synthetic_data,
    get_origin_data,
    plot_analysis,
    write_report,
)

if __name__ == "__main__":
    try:
        # Read sample data.csv file locally (10k rows)
        root = Path(__file__).parent.parent
        path = root / "data.csv"
        real_data, metadata = get_origin_data(path)

        # Generate synthetic data
        synthetic_data = generate_synthetic_data(real_data, metadata)

        # Analyze data
        diagnostic, quality_report = analyze_data(real_data, synthetic_data, metadata)

        # Write reports and plots
        plot_analysis(root, real_data, synthetic_data, metadata)
        write_report(root, diagnostic, quality_report, synthetic_data)

    except RuntimeError as e:
        print(f"Error occurred during runtime: {e}")
        exit(1)
