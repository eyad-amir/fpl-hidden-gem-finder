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
  response.raise_for_status()
  payload = response.json()

  if "elements" not in payload or "element_types" not in payload:
    raise ValueError("FPL API response is missing elements or element_types.")

  players = pd.DataFrame(payload["elements"])
  positions = pd.DataFrame(payload["element_types"])[
    ["id", "singular_name"]
  ].rename(columns={"id": "element_type", "singular_name": "position_name"})
  data = players.merge(
    positions,
    on="element_type",
    how="left",
    validate="many_to_one",
  )
  numeric_columns = ["now_cost", "total_points", "minutes", "selected_by_percent"]
  for column in numeric_columns:
    if column in data:
      data[column] = pd.to_numeric(data[column], errors="coerce")
  data["now_cost"] = data["now_cost"] / 10
  return data
