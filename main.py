
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import pickle
import os
import pathlib

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load scaler for preprocessing (no label encoder needed)
SCALER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scaler.pkl'))
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xgboost_model.pkl'))

try:
    with open(MODEL_PATH, 'rb') as f:
        xgb_model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
except Exception as e:
    import sys
    print(f"Failed to load model or scaler: {e}", file=sys.stderr)
    xgb_model = None
    scaler = None

# Features order as in the new model (without City)
FEATURES = ['CO', 'NO2', 'SO2', 'O3', 'PM2.5', 'PM10']




@app.post("/predict")
async def predict(features: dict):
    if xgb_model is None or scaler is None:
        return JSONResponse(status_code=500, content={"error": "Model or scaler not loaded on server."})
    try:
        # Preprocess input
        input_data = features.copy()
        # Build feature array (no City)
        X = np.array([[float(input_data.get(feat, 0)) for feat in FEATURES]])
        # Scale features
        X_scaled = scaler.transform(X)
        pred = xgb_model.predict(X_scaled)
        return {"prediction": float(pred[0])}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


# Serve the entire frontend directory at root
frontend_path = pathlib.Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
