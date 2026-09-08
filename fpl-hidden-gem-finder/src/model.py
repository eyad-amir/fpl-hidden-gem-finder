"""
Modeling functions for the FPL Hidden Gem Finder project.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression


def time_based_split(df: pd.DataFrame, train_gw_end: int, test_gw_start: int):
    """
    Split the DataFrame into train/test sets chronologically by gameweek.

    IMPORTANT: Do NOT use sklearn's train_test_split(shuffle=True) here.
    This is time-series-like data — randomly shuffling gameweeks means the
    model could train on a later gameweek and test on an earlier one,
    which leaks future information into training. Always split so that
    training gameweeks come strictly before test gameweeks.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a gameweek column (e.g. 'round' or 'gameweek').
    train_gw_end : int
        Last gameweek (inclusive) to include in the training set.
    test_gw_start : int
        First gameweek (inclusive) to include in the test set.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (train_df, test_df)
    """
    raise NotImplementedError


def train_baseline_model(train_df: pd.DataFrame):
    """
    Build a naive baseline: predict each player's next-gameweek points as
    their historical average points so far. This is what your real model
    needs to beat to prove it's adding value.

    Parameters
    ----------
    train_df : pd.DataFrame

    Returns
    -------
    dict or pd.Series
        Mapping of player id -> baseline predicted points.
    """
    raise NotImplementedError


def train_linear_regression(train_df: pd.DataFrame, features: list, target: str) -> LinearRegression:
    """
    Train a scikit-learn LinearRegression model on the given features.

    Parameters
    ----------
    train_df : pd.DataFrame
    features : list of str
        Column names to use as model inputs.
    target : str
        Column name of the value to predict (e.g. next gameweek's points).

    Returns
    -------
    LinearRegression
        The fitted model.
    """
    raise NotImplementedError


def evaluate_model(model, test_df: pd.DataFrame, features: list, target: str) -> dict:
    """
    Evaluate a fitted model on the test set.

    Parameters
    ----------
    model : fitted sklearn estimator
    test_df : pd.DataFrame
    features : list of str
    target : str

    Returns
    -------
    dict
        e.g. {"r2": ..., "mae": ...}
        Also consider comparing against the baseline's R²/MAE to show
        whether the model actually adds value.
    """
    raise NotImplementedError
