"""
Verifying schema for data we receive and converting them into expected data types.

Schema should be named `*_schema` and they should typically have a concomitant
`check_and_cast_*_schema` function.

The output of `check_and_cast_*_schema` should generally be saved to a parquet file.
"""
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from pandera import Check, Column, DataFrameSchema


@extensions.register_check_method(
    statistics=["val"],
    check_type="element_wise",
)
def date_length(element, *, val):
    """
    Element-wise check of value lengths
    """
    return len(element) == val


@extensions.register_check_method(
    statistics=["val"],
    check_type="element_wise",
)
def ssn_length(element, *, min_value, max_value):
    """
    Element-wise check of values between min_value and max_value
    """
    return (min_value <= element) & (element <= max_value)


example_schema = DataFrameSchema(
    columns={
        "SSN": Column(
            int,
            checks=Check.ssn_length(min_value=1_01_0001, max_value=999_99_9999),
        ),
        "START_DATE": Column(
            str,
            checks=Check.date_length(8),
        ),
        "RAND_NBR": Column(int),
        "SENT_DATE": Column(
            str,
            nullable=True,
        ),
    },
    strict="filter",  # drop all unnecessary columns
    coerce=True,
)


@pa.check_input(example_schema)
def check_and_cast_example_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dates to actual pandas datetimes and change names to snake_case
    """
    df.rename(columns={key: key.lower() for key in df}, inplace=True)
    for key in df:
        if key.endswith("date"):
            df[key] = pd.to_datetime(df[key], format="%Y%m%d")
    return df
