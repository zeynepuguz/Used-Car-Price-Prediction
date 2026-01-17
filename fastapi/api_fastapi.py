from fastapi import FastAPI
from src.schemas import CarRequest
from src.predict import predict_range, load_models

app = FastAPI(title="Car Price Prediction API", version="1.0.0")

@app.on_event("startup")
def _warmup():
    load_models()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: CarRequest):
    return {"price_range": predict_range(payload.model_dump())}
