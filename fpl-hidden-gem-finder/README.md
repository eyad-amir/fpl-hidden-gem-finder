# FPL Hidden Gem Finder

## Project Overview
An exploratory data analysis and prediction dashboard for Fantasy Premier League (FPL).
The goal is to identify budget-friendly "enabler" players and efficient picks using
custom metrics (Points Per Million, custom fixture difficulty) and a simple linear
regression model to predict next-gameweek points.

## Dataset Source
[Fantasy Premier League 2025-2026 — Kaggle](https://www.kaggle.com/datasets/calvinrostanto/fantasy-premier-league-2025-2026)

Place the raw CSV in `data/raw/` before running the notebook.

## Setup Instructions
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the notebook first (`notebooks/01_eda_and_feature_engineering.ipynb`) to clean the
data and save a processed file to `data/processed/`. Then run the dashboard:
```bash
streamlit run app.py
```

## Project Structure
```
fpl-hidden-gem-finder/
├── data/
│   ├── raw/              # original Kaggle CSV (not tracked in git)
│   └── processed/        # cleaned data saved as .parquet
├── notebooks/
│   └── 01_eda_and_feature_engineering.ipynb
├── src/
│   ├── data_cleaning.py       # loading + cleaning functions
│   ├── feature_engineering.py # rolling form, fixture difficulty, points per million
│   └── model.py               # time-based split, baseline, linear regression, evaluation
├── app.py                # Streamlit dashboard
└── requirements.txt
```

## Key Findings
_(fill in after analysis — e.g. model performance vs baseline, most efficient players found, limitations)_
