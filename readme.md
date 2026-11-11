# Bangalore Home Price Prediction
https://real-estate-price-prediction-nbjv.onrender.com/

Predicts residential property prices in Bangalore. Linear regression model served via a Flask API with a vanilla JS frontend.

## Stack

- Python, Flask, Gunicorn, scikit-learn
- HTML / CSS / JS

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cd server
python server.py
```

App runs at `http://localhost:5000`.

## Test

```bash
python -m unittest discover -s tests
```

## API

```bash
# locations
GET /api/get_location_names

# predict
POST /api/predict_home_price
{"total_sqft": 1000, "bhk": 2, "bath": 2, "location": "Indira Nagar"}
```

## Deploy

Connects straight to Render — just link the repo and it picks up the `Procfile`.
