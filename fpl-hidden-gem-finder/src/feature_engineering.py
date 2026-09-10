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
    result = df.copy()
    cost = pd.to_numeric(result["now_cost"], errors="coerce")
    points = pd.to_numeric(result["total_points"], errors="coerce")
    result["points_per_million"] = points.div(cost.where(cost > 0))
    return result


def add_gem_score(
    df: pd.DataFrame,
    points_weight: float = 0.75,
    ownership_weight: float = 0.25,
) -> pd.DataFrame:
    """Add a normalized score for efficient, low-owned players.

    The ownership bonus is ``max_ownership - selected_by_percent``. Both
    components are normalized to 0-1 before weighting because they use
    different units.
    """
    if points_weight < 0 or ownership_weight < 0:
        raise ValueError("Score weights must be non-negative.")
    if points_weight + ownership_weight == 0:
        raise ValueError("At least one score weight must be greater than zero.")

    result = add_points_per_million(df)
    ownership = pd.to_numeric(result["selected_by_percent"], errors="coerce")
    inverse_ownership = ownership.max() - ownership
    ppm_max = result["points_per_million"].max()
    inverse_max = inverse_ownership.max()
    normalized_ppm = result["points_per_million"].div(ppm_max) if ppm_max > 0 else 0
    normalized_ownership = inverse_ownership.div(inverse_max) if inverse_max > 0 else 0
    total_weight = points_weight + ownership_weight
    result["gem_score"] = (
        points_weight * normalized_ppm + ownership_weight * normalized_ownership
    ) / total_weight
    return result


