"""
Data cleaning functions for the FPL Hidden Gem Finder project.
"""

from typing import Final

import pandas as pd
import requests


FPL_API_URL: Final[str] = "https://fantasy.premierleague.com/api/bootstrap-static/"


def fetch_fpl_data(url: str = FPL_API_URL) -> pd.DataFrame:
  """Fetch current player data and readable position names from the FPL API.

  The API stores player prices in tenths of a million, so ``now_cost`` is
  converted from values such as ``55`` to ``5.5``.
  """
  response = requests.get(url, timeout=30)
    "total_points",
    "minutes",
    "opponent_team",
  ]
  for column in numeric_columns:
    if column in history:
      history[column] = pd.to_numeric(history[column], errors="coerce")

  if players is not None:
    metadata_columns = [
      column
      for column in ["id", "web_name", "team", "element_type", "position_name"]
      if column in players.columns
    ]
    if "id" in metadata_columns:
      metadata = players[metadata_columns].rename(columns={"id": "player_id"})
      history = history.merge(metadata, on="player_id", how="left", validate="many_to_one")

  return history.sort_values(["player_id", "gameweek"]).reset_index(drop=True)
