from pathlib import Path
import datetime
import joblib
import pandas as pd
import numpy as np
import catboost as cb

BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_Q25_PATH = ARTIFACTS_DIR / "model_q25.joblib"
MODEL_Q50_PATH = ARTIFACTS_DIR / "model_q50.joblib"
MODEL_Q75_PATH = ARTIFACTS_DIR / "model_q75.joblib"

FEATURE_ORDER = [
    "model",
    "transmission",
    "mileage",
    "fuelType",
    "tax",
    "mpg",
    "engineSize",
    "age",
]

CAT_COLS = ["model", "transmission", "fuelType"]

_models = {}


def load_models():
    global _models
    if not _models:
        _models["q25"] = joblib.load(MODEL_Q25_PATH)
        _models["q50"] = joblib.load(MODEL_Q50_PATH)
        _models["q75"] = joblib.load(MODEL_Q75_PATH)
    return _models


def normalize_input(payload: dict) -> dict:
    model_name = payload.get("model") or payload.get("car_model")
    if not model_name:
        raise KeyError("model")

    if "mileage" in payload:
        mileage = int(payload["mileage"])
    elif "km" in payload:
        mileage = int(payload["km"])
    else:
        raise KeyError("mileage")

    fuel_type = payload.get("fuelType") or payload.get("fuel")
    if not fuel_type:
        raise KeyError("fuelType")

    if "age" in payload:
        age = int(payload["age"])
    elif "year" in payload:
        age = max(0, datetime.datetime.now().year - int(payload["year"]))
    else:
        raise KeyError("age")

    return {
        "model": str(model_name),
        "transmission": str(payload["transmission"]),
        "mileage": mileage,
        "fuelType": str(fuel_type),
        "tax": int(payload["tax"]),
        "mpg": float(payload["mpg"]),
        "engineSize": float(payload["engineSize"]),
        "age": age,
    }


def _predict_log(model: cb.CatBoostRegressor, X: pd.DataFrame) -> float:
    cat_idx = [X.columns.get_loc(c) for c in CAT_COLS]
    pool = cb.Pool(X, cat_features=cat_idx)
    return float(model.predict(pool)[0])


def predict_range(payload: dict) -> dict:
    models = load_models()
    feats = normalize_input(payload)

    X = pd.DataFrame([[feats[c] for c in FEATURE_ORDER]], columns=FEATURE_ORDER)

    p25 = np.expm1(_predict_log(models["q25"], X))
    p50 = np.expm1(_predict_log(models["q50"], X))
    p75 = np.expm1(_predict_log(models["q75"], X))

    return {
        "min": int(round(min(p25, p50, p75))),
        "recommended": int(round(p50)),
        "max": int(round(max(p25, p50, p75))),
        "currency": "GBP",
    }
