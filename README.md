# FPL Hidden Gem Finder

An interpretable Streamlit dashboard for finding Fantasy Premier League players
who combine strong output, good value, and low ownership.

## What it does

The dashboard loads current player data from the official FPL API and provides:

- Maximum-price filtering
- Maximum-ownership filtering
- Position filtering
- A sortable player results table
- A price-versus-total-points scatter plot
- A transparent Gem Score ranking

This release uses a hand-weighted scoring formula rather than a trained machine
learning model.

## Gem Score

Each score combines two normalized components:

```text
Gem Score = 75% normalized points per million
		  + 25% normalized inverse ownership
```

Where:

- `points per million = total_points / price`
- `inverse ownership = max ownership - player ownership`

Both components are normalized to a 0–1 range before applying the weights.
This means cheaper, productive, and less-owned players receive higher scores.

## Data source

Player data comes from the official FPL `bootstrap-static` endpoint:

<https://fantasy.premierleague.com/api/bootstrap-static/>

The API returns prices in tenths of a million. For example, `55` represents
£5.5m. The application converts these values before calculating the score.

## Setup

From the project directory:

```bash
python -m venv venv
```

Activate the environment:

```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the dashboard

```bash
streamlit run app.py
```

The app opens in your browser. It requires an internet connection because the
player data is fetched from the live FPL API when the app starts.

## Project structure

```text
fpl-hidden-gem-finder/
├── app.py                         # Streamlit dashboard
├── requirements.txt               # Python dependencies
├── src/
│   ├── data_cleaning.py           # API loading and data cleaning
│   └── feature_engineering.py     # Value metrics and Gem Score
├── notebooks/
│   └── 01_eda_and_feature_engineering.ipynb
└── data/
	├── raw/                       # Optional local data files
	└── processed/                 # Optional generated outputs
```

## Limitations

The Gem Score is a ranking heuristic, not a prediction of future points. It
does not currently account for fixture difficulty, expected minutes, injuries,
rotation risk, or upcoming opponent strength. Use it as a shortlist for further
FPL research rather than as an automatic team-selection system.

## License

This project is intended for educational and portfolio use. FPL data is
provided by the official Fantasy Premier League API.
