"""
Data cleaning functions for the FPL Hidden Gem Finder project.
"""

import pandas as pd


def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """
    Load the raw FPL CSV and return a cleaned DataFrame.

    Steps this function should perform:
    - Load the CSV from `filepath`.
    - Check for and handle duplicate rows (a player can sometimes appear
      twice for the same gameweek in scraped data — verify this on the
      actual file before deciding how to drop duplicates).
    - Handle missing values in minutes-played / points columns deliberately.
      A player with 0 minutes is a real signal (didn't play), not missing
      data — don't blindly dropna().
    - Convert `now_cost` to actual millions if it's stored as an integer
      (e.g. 55 -> 5.5), matching the raw FPL API convention. Check whether
      this dataset already did that conversion before applying it again.
    - Ensure the DataFrame is sorted by player id and gameweek, since later
      feature engineering (rolling averages) depends on correct ordering.

    Parameters
    ----------
    filepath : str
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned, sorted DataFrame ready for feature engineering.
    """
    raise NotImplementedError
