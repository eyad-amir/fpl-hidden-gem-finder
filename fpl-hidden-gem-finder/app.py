"""
FPL Hidden Gem Finder — Streamlit dashboard entry point.
"""

import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(
    page_title="FPL Hidden Gem Finder",
    layout="wide",
)

st.title("FPL Hidden Gem Finder")
st.caption("Finding budget-friendly enablers and efficient picks with data.")


# --- Data loading ---
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """
    Load the processed (already cleaned + feature-engineered) dataset.
    Replace this with the actual path to your data/processed/*.parquet file
    once Phase 1-2 (notebook) are done.
    """
    # df = pd.read_parquet(path)
    # return df
    raise NotImplementedError


# data = load_data("data/processed/fpl_processed.parquet")


# --- Sections ---
st.header("Filter Players")
# TODO: position filter, price range slider, team filter, min minutes filter

st.header("Points per Million Explorer")
# TODO: scatter plot (price vs total points, colored by position),
# with hidden gems = cheap + high points highlighted

st.header("Next Gameweek Predictions")
# TODO: table of predicted points per player from the trained model,
# sortable, with a note on model limitations (R²/MAE vs baseline)
