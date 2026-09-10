"""Simple, interpretable models for next-gameweek FPL points."""

from typing import Sequence

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def time_based_split(
    df: pd.DataFrame,
    train_gw_end: int,
    test_gw_start: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split rows chronologically by gameweek without shuffling.

    Randomly shuffling this data can put later gameweeks in the training set
    and earlier gameweeks in the test set. That leaks future information into
    training and makes evaluation unrealistically optimistic.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a ``gameweek`` column.
    train_gw_end : int
        Last gameweek included in training.
    test_gw_start : int
        First gameweek included in testing.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Chronological ``(train_df, test_df)``.
    """
    if "gameweek" not in df.columns:
        raise ValueError("DataFrame must contain a 'gameweek' column.")
    if train_gw_end >= test_gw_start:
        raise ValueError("train_gw_end must be before test_gw_start.")

    gameweeks = pd.to_numeric(df["gameweek"], errors="coerce")
    if gameweeks.isna().any():
        raise ValueError("gameweek must contain numeric values.")

    train_df = df.loc[gameweeks <= train_gw_end].copy()
    test_df = df.loc[gameweeks >= test_gw_start].copy()
    return train_df, test_df


def train_baseline_model(train_df: pd.DataFrame) -> pd.Series:
    """Predict each player's points with their historical training average.

    The returned Series is indexed by ``player_id`` and must be created from
    training rows only. It provides the benchmark that the regression model
    needs to beat.
    """
    required_columns = {"player_id", "total_points"}
    missing_columns = required_columns.difference(train_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    baseline = train_df.groupby("player_id")["total_points"].mean()
    baseline.name = "baseline_prediction"
    return baseline


def train_linear_regression(
    train_df: pd.DataFrame,
    features: Sequence[str],
    target: str,
) -> LinearRegression:
    """Fit an ordinary least-squares linear regression model.

    Rows with missing feature or target values are excluded because the rolling
    features are undefined for a player's first gameweek.
    """
    columns = list(features) + [target]
    missing_columns = set(columns).difference(train_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    training_data = train_df[columns].dropna()
    if training_data.empty:
        raise ValueError("No complete rows are available for model training.")

    model = LinearRegression()
    model.fit(training_data[list(features)], training_data[target])
    return model


def evaluate_model(
    model: LinearRegression,
    test_df: pd.DataFrame,
    features: Sequence[str],
    target: str,
    baseline_predictions: pd.Series,
) -> dict[str, float]:
    """Compare regression and historical-average baseline predictions.

    ``baseline_predictions`` should come from ``train_baseline_model`` and be
    indexed by ``player_id``. Positive ``mae_improvement`` means the regression
    has lower error; positive ``r2_improvement`` means it explains more
    variance than the baseline.
    """
    columns = list(features) + [target, "player_id"]
    missing_columns = set(columns).difference(test_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    evaluation_data = test_df[columns].dropna().copy()
    if evaluation_data.empty:
        raise ValueError("No complete rows are available for evaluation.")

    model_predictions = model.predict(evaluation_data[list(features)])
    baseline = evaluation_data["player_id"].map(baseline_predictions)
    valid_baseline = baseline.notna()
    if not valid_baseline.any():
        raise ValueError("No test players have a baseline prediction.")

    actual = evaluation_data.loc[valid_baseline, target]
    baseline_values = baseline.loc[valid_baseline]
    model_values = pd.Series(model_predictions, index=evaluation_data.index).loc[
        valid_baseline
    ]

    model_r2 = r2_score(actual, model_predictions)
    model_mae = mean_absolute_error(actual, model_predictions)
    baseline_r2 = r2_score(actual, baseline_values)
    baseline_mae = mean_absolute_error(actual, baseline_values)

    return {
        "model_r2": model_r2,
        "model_mae": model_mae,
        "baseline_r2": baseline_r2,
        "baseline_mae": baseline_mae,
        "r2_improvement": model_r2 - baseline_r2,
        "mae_improvement": baseline_mae - mean_absolute_error(actual, model_values),
    }
