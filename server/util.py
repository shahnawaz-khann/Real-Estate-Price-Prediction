import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "banglore_home_prices_model.pickle"
COLUMNS_PATH = ARTIFACT_DIR / "columns.json"

__locations = None
__data_columns = None
__model = None


def _ensure_legacy_sklearn_compatibility():
    """Allow older pickled sklearn estimators to load under newer sklearn versions."""
    try:
        from sklearn.linear_model import _base as sklearn_base

        sys.modules.setdefault("sklearn.linear_model.base", sklearn_base)
    except Exception:
        pass


def _normalize_location_name(location):
    return str(location).strip().lower()


def get_estimated_price(location, sqft, bhk, bath):
    if __data_columns is None or __model is None:
        load_saved_artifacts()

    normalized_location = _normalize_location_name(location)
    try:
        loc_index = __data_columns.index(normalized_location)
    except ValueError:
        loc_index = -1

    # Reject entirely unknown locations (not in training data and not 'other').
    # 'other' is a catch-all bucket trained on rare locations, so it stays valid.
    if loc_index < 0 and normalized_location != "other":
        raise ValueError(f"Location '{location}' is not in the trained model.")

    x = pd.DataFrame([np.zeros(len(__data_columns), dtype=float)], columns=__data_columns)
    x.iloc[0, 0] = float(sqft)
    x.iloc[0, 1] = float(bath)
    x.iloc[0, 2] = float(bhk)
    if loc_index >= 0:
        x.iloc[0, loc_index] = 1.0

    estimated_price = float(__model.predict(x)[0])
    return round(estimated_price, 2)


def load_saved_artifacts():
    global __data_columns, __locations, __model

    if __data_columns is not None and __model is not None:
        return

    print("loading saved artifacts...start")

    with COLUMNS_PATH.open("r", encoding="utf-8") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    if __model is None:
        try:
            with MODEL_PATH.open("rb") as f:
                __model = pickle.load(f)
        except ModuleNotFoundError:
            _ensure_legacy_sklearn_compatibility()
            with MODEL_PATH.open("rb") as f:
                __model = pickle.load(f)

        if not hasattr(__model, "positive"):
            __model.positive = False

    print("loading saved artifacts...done")


def get_location_names():
    if __locations is None:
        load_saved_artifacts()
    return __locations


def get_data_columns():
    if __data_columns is None:
        load_saved_artifacts()
    return __data_columns


if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names()[:5])
    print(get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))
    print(get_estimated_price("Indira Nagar", 1000, 2, 2))
    print(get_estimated_price("Kalhalli", 1000, 2, 2))