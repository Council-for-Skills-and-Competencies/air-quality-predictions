# Air Quality Prediction Web App

## Backend (FastAPI)
- Location: `backend/`
- Run with: `uvicorn main:app --reload`
- Serves a `/predict` endpoint for AQI prediction using the trained XGBoost model.

## Frontend (HTML/JS/CSS)
- Location: `frontend/`
- Open `frontend/index.html` in your browser.
- Enter feature values and click Predict to get AQI from the backend.

## Integration
- The frontend sends a POST request to the FastAPI backend at `http://127.0.0.1:8000/predict`.
- Ensure the backend is running before using the frontend.

## Requirements
- Python 3.8+
- Packages: fastapi, uvicorn, pandas, numpy, scikit-learn, xgboost

## Model
- The trained XGBoost model is loaded from `xgboost_model.pkl` in the project root.

---

**Tip:**
- If you want to serve the frontend from FastAPI, uncomment the `StaticFiles` lines in `backend/main.py` and adjust the directory path.
