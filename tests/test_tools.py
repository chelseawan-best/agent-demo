import pytest

from agent_demo.tools import (
    calculate_correlation,
    dataset_overview,
    describe_numeric_column,
    load_dataset,
)

DATA_PATH = "data/sample.csv"


def test_load_dataset_reads_csv() -> None:
    dataframe = load_dataset(DATA_PATH)
    assert dataframe.shape == (12, 7)
    assert dataframe["customer_id"].iloc[0] == "C001"


def test_load_dataset_rejects_missing_file() -> None:
    with pytest.raises(FileNotFoundError, match="Dataset file not found"):
        load_dataset("data/does_not_exist.csv")


def test_dataset_overview_reports_missing_values() -> None:
    result = dataset_overview(DATA_PATH)
    assert result["row_count"] == 12
    assert result["column_count"] == 7
    assert result["missing_values"]["tenure_months"] == 1
    assert result["missing_values"]["weekly_usage_hours"] == 1


def test_describe_numeric_column() -> None:
    result = describe_numeric_column(DATA_PATH, "monthly_price")
    assert result["count"] == 12
    assert result["mean"] == pytest.approx(26.6666667)
    assert result["median"] == 25.0


def test_calculate_correlation_uses_complete_pairs() -> None:
    result = calculate_correlation(
        DATA_PATH,
        "weekly_usage_hours",
        "churned",
    )
    assert result["observation_count"] == 11
    assert result["pearson_correlation"] == pytest.approx(-0.73134975)