"""Streamlit dashboard for finding low-cost, low-owned FPL players."""

import plotly.express as px
import streamlit as st

from src.data_cleaning import fetch_fpl_data
from src.feature_engineering import add_gem_score


st.set_page_config(page_title="FPL Hidden Gem Finder", layout="wide")
st.title("FPL Hidden Gem Finder")
st.caption("A transparent 75% points-per-million and 25% low-ownership score.")

try:
    players = add_gem_score(fetch_fpl_data())
except Exception as error:
    st.error(f"Could not load the FPL API data: {error}")
    st.stop()

st.header("Filter players")
max_price = st.slider(
    "Maximum price (£m)",
    min_value=float(players["now_cost"].min()),
    max_value=float(players["now_cost"].max()),
    value=float(players["now_cost"].max()),
    step=0.1,
)
max_ownership = st.slider(
    "Maximum ownership (%)",
    min_value=0.0,
    max_value=float(players["selected_by_percent"].max()),
    value=float(players["selected_by_percent"].max()),
    step=0.1,
)
positions = sorted(players["position_name"].dropna().unique())
selected_positions = st.multiselect("Positions", positions, default=positions)

filtered = players[
    (players["now_cost"] <= max_price)
    & (players["selected_by_percent"] <= max_ownership)
    & (players["position_name"].isin(selected_positions))
].sort_values("gem_score", ascending=False)

st.subheader(f"Results ({len(filtered)} players)")
table_columns = [
    "web_name",
    "position_name",
    "now_cost",
    "total_points",
    "selected_by_percent",
    "points_per_million",
    "gem_score",
]
st.dataframe(
    filtered[table_columns].rename(
        columns={
            "web_name": "Player",
            "position_name": "Position",
            "now_cost": "Price (£m)",
            "total_points": "Total points",
            "selected_by_percent": "Ownership (%)",
            "points_per_million": "Points / £m",
            "gem_score": "Gem Score",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Price versus total points")
fig = px.scatter(
    filtered,
    x="now_cost",
    y="total_points",
    color="position_name",
    hover_name="web_name",
    labels={
        "now_cost": "Price (£m)",
        "total_points": "Total points",
        "position_name": "Position",
    },
)
st.plotly_chart(fig, use_container_width=True)
