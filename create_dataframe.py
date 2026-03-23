"""Module for creating sample pandas DataFrames."""

import pandas as pd
from typing import Any


def createSampleDataFrame() -> pd.DataFrame:
    """
    Create a sample pandas DataFrame with 3 columns and 5 rows.

    Returns:
        pd.DataFrame: A DataFrame with columns 'Column1', 'Column2', and 'Column3',
                      containing 5 rows of sample data.

    Example:
        >>> df = createSampleDataFrame()
        >>> print(df)
           Column1 Column2  Column3
        0        1       A     10.5
        1        2       B     20.3
        2        3       C     15.7
        3        4       D     25.1
        4        5       E     30.9
    """
    data: dict[str, Any] = {
        "Column1": [1, 2, 3, 4, 5],
        "Column2": ["A", "B", "C", "D", "E"],
        "Column3": [10.5, 20.3, 15.7, 25.1, 30.9],
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = createSampleDataFrame()
    print(df)
    print("\nDataframe shape:", df.shape)
    print("\nDataframe info:")
    print(df.info())
