"""
Feature engineering functions for the FPL Hidden Gem Finder project.
"""

import pandas as pd


def add_points_per_million(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a `points_per_million` column: total_points / now_cost.

    This is the core EDA metric for finding budget-friendly "enabler"
    players. Watch for division-by-zero or missing cost values.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Same DataFrame with a new `points_per_million` column.
    """
    raise NotImplementedError


def add_rolling_form(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """
    Add a `rolling_form_{window}gw` column: rolling average of a player's
    points over the last `window` gameweeks.

    IMPORTANT — DATA LEAKAGE WARNING:
    You MUST `.shift(1)` before applying `.rolling(window).mean()`.
    Without the shift, a given gameweek's rolling average will include
    that same gameweek's own points — meaning the model would effectively
    see the answer before predicting it. Compute this per player
    (group by player id) to avoid mixing rolling windows across players.

    Parameters
    ----------
    df : pd.DataFrame
    window : int
        Number of past gameweeks to average over.

    Returns
    -------
    pd.DataFrame
        Same DataFrame with a new rolling form column.
    """
    raise NotImplementedError


def add_custom_fixture_difficulty(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a custom fixture difficulty score, built from the opponent's
    recent defensive record (e.g. goals conceded or xG conceded over
    their last N games), rather than relying on the official FPL FDR
    (which is known to be a weak, largely static metric).

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Same DataFrame with a new fixture difficulty column.
    """
    raise NotImplementedError


def add_minutes_reliability(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Add a `minutes_reliability` column: rolling average of minutes played
    over the last `window` gameweeks, to flag rotation/bench risk.

    Same leakage caution as add_rolling_form applies here — shift before
    rolling.

    Parameters
    ----------
    df : pd.DataFrame
    window : int

    Returns
    -------
    pd.DataFrame
        Same DataFrame with a new minutes reliability column.
    """
    raise NotImplementedError
