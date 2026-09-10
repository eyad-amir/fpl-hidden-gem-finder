# FPL Hidden Gem Finder

## Project Overview
A small Streamlit dashboard for finding cheap, high-performing, low-owned
Fantasy Premier League players. It uses a transparent hand-weighted formula,
not a trained machine learning model:

```text
Gem Score = 75% normalized points-per-million
		  + 25% normalized (max ownership - player ownership)
```

The dashboard loads current player data from the official FPL API:
`https://fantasy.premierleague.com/api/bootstrap-static/`.

## Setup Instructions
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the dashboard from the project directory:
```bash
streamlit run app.py
```

## Project Structure
```
fpl-hidden-gem-finder/
├── data/
│   ├── raw/              # optional historical CSV data
│   └── processed/        # optional notebook outputs
├── notebooks/
│   └── 01_eda_and_feature_engineering.ipynb
├── src/
│   ├── data_cleaning.py       # API loading and position/price cleaning
│   └── feature_engineering.py # points per million and Gem Score
├── app.py                # Streamlit dashboard
└── requirements.txt
```

## Notes

The API price field is stored in tenths of a million (for example, `55` means
£5.5m). `fetch_fpl_data` converts it to real millions before the dashboard
calculates scores.

The notebook is retained as historical exploratory work. The deployed app does
not use its unfinished modeling pipeline; the supported runtime is `app.py`.
