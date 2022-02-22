from pathlib import Path

import pandas as pd
import pandera as pa
import pytest

from pyutils.schema import check_and_cast_example_schema


@pytest.fixture(scope="module")
def example_df(fixtures_path: Path) -> pd.DataFrame:
    return pd.read_csv(fixtures_path / "example_data.csv")


def test_check_and_cast_example_schema(example_df: pd.DataFrame):
    df = check_and_cast_example_schema(example_df)

    # Only keep relevant columns
    assert set(df.columns) == {"ssn", "start_date", "rand_nbr", "sent_date"}

    with pytest.raises(pa.errors.SchemaError):
        example_df_prime = example_df.copy()
        # An out of bounds SSN
        example_df_prime.loc[0, "SSN"] = "001000000"

        check_and_cast_example_schema(example_df_prime)

    # Dates are as expected
    assert df["start_date"].max() == pd.to_datetime("2022-01-02")
    assert df["sent_date"].max() == pd.to_datetime("2022-01-03")
    assert df["sent_date"].notna().sum() == 1
    assert df["start_date"].notna().sum() == 2

    assert len(df) == 2
