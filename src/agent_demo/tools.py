from pathlib import Path

import pandas as pd


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """Load and validate a non-empty CSV dataset."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Dataset must be a CSV file: {path}")

    dataframe = pd.read_csv(path)
    if dataframe.empty:
        raise ValueError(f"Dataset is empty: {path}")

    return dataframe


def dataset_overview(file_path: str | Path) -> dict:
    """Return dataset dimensions, columns, and missing-value counts."""
    dataframe = load_dataset(file_path)
    missing_values = {
        str(column): int(count)
        for column, count in dataframe.isna().sum().items()
    }
    return {
        "row_count": int(dataframe.shape[0]),
        "column_count": int(dataframe.shape[1]),
        "columns": dataframe.columns.tolist(),
        "missing_values": missing_values,
    }


def describe_numeric_column(file_path: str | Path, column: str) -> dict:
    """Return descriptive statistics for one numeric column."""
    dataframe = load_dataset(file_path)

    if column not in dataframe.columns:
        raise ValueError(f"Unknown column: {column}")
    if not pd.api.types.is_numeric_dtype(dataframe[column]):
        raise ValueError(f"Column is not numeric: {column}")

    series = dataframe[column].dropna()
    return {
        "column": column,
        "count": int(series.count()),
        "missing_count": int(dataframe[column].isna().sum()),
        "mean": float(series.mean()),
        "median": float(series.median()),
        "standard_deviation": float(series.std()),
        "minimum": float(series.min()),
        "maximum": float(series.max()),
    }


def calculate_correlation(
    file_path: str | Path,
    column_x: str,
    column_y: str,
) -> dict:
    """Calculate Pearson correlation between two numeric columns."""
    dataframe = load_dataset(file_path)

    for column in (column_x, column_y):
        if column not in dataframe.columns:
            raise ValueError(f"Unknown column: {column}")
        if not pd.api.types.is_numeric_dtype(dataframe[column]):
            raise ValueError(f"Column is not numeric: {column}")

    paired_data = dataframe[[column_x, column_y]].dropna()
    if len(paired_data) < 2:
        raise ValueError("At least two complete observations are required")

    return {
        "column_x": column_x,
        "column_y": column_y,
        "observation_count": int(len(paired_data)),
        "pearson_correlation": float(
            paired_data[column_x].corr(paired_data[column_y])
        ),
    }