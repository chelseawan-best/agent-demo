from pathlib import Path
from typing import Annotated

from agent_framework import tool

from agent_demo.tools import (
    calculate_correlation,
    dataset_overview,
    describe_numeric_column,
)


DATA_PATH = Path(__file__).parents[2] / "data" / "sample.csv"


@tool(approval_mode="never_require")
def get_dataset_overview() -> dict:
    """Inspect the dataset structure, columns, and missing-value counts."""
    return dataset_overview(DATA_PATH)


@tool(approval_mode="never_require")
def get_column_statistics(
    column: Annotated[str, "Name of the numeric column to summarize"],
) -> dict:
    """Calculate descriptive statistics for one numeric dataset column."""
    return describe_numeric_column(DATA_PATH, column)


@tool(approval_mode="never_require")
def get_correlation(
    column_x: Annotated[str, "Name of the first numeric column"],
    column_y: Annotated[str, "Name of the second numeric column"],
) -> dict:
    """Calculate Pearson correlation between two numeric dataset columns."""
    return calculate_correlation(DATA_PATH, column_x, column_y)