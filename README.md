# Used Car Price Prediction & Fair Pricing System

This project focuses on predicting used car prices based on vehicle characteristics and providing
**transparent and actionable pricing recommendations** for sellers.

Instead of producing a single point estimate, the system predicts a **fair price range** using
**quantile regression** and explains predictions using **SHAP**.

---

## Motivation

Pricing a used car is inherently uncertain:

- Overpricing discourages buyers
- Underpricing may reduce trust or cause financial loss
- Market prices vary due to negotiation, demand, and seller urgency

This project addresses these challenges by combining:
- Robust machine learning models
- Explainable AI techniques
- Price uncertainty modeling

---

## Exploratory Data Analysis (EDA)

### Price Distribution
Used car prices are heavily right-skewed, with most vehicles concentrated in lower price ranges.

![Price Distribution](graphics/output.png)

---

### Log-Transformed Price Distribution
Prices were log-transformed to reduce skewness and stabilize variance.

![Log Price Distribution](graphics/output1.png)

---

### Vehicle Age vs Price
Vehicle prices decrease as age increases, showing a strong nonlinear relationship.

![Age vs Price](graphics/output2.png)

---

### Mileage vs Price
Higher mileage is clearly associated with lower prices.

![Mileage vs Price](graphics/output3.png)

---

### Price Distribution by Fuel Type
Fuel type influences pricing, with electric and hybrid vehicles generally priced higher.

![Fuel Type vs Price](graphics/output4.png)

---

### Price Distribution by Transmission Type
Automatic vehicles tend to have higher prices than manual ones.

![Transmission vs Price](graphics/output5.png)

---

### Engine Size vs Price
Larger engine sizes are associated with higher prices, with increasing variance.

![Engine Size vs Price](graphics/output6.png)

---

## Model Training

### Model Choice
- **CatBoostRegressor**
- Native support for categorical variables
- Strong performance on tabular data
- Robust to nonlinear interactions

The target variable was modeled as **log(price)**.

---

### Model Performance
- **Test MAE:** approximately **£1,142**

This error level is acceptable in the used car market, where negotiation and seller behavior
introduce natural variability.

---

## Model Explainability with SHAP

### Global Feature Importance
SHAP summary plots show the most influential features.

![SHAP Summary](graphics/output7.png)

Key drivers:
- Vehicle model
- Vehicle age
- Engine size
- Mileage

---

### Local Explanation (Single Vehicle)
Waterfall plots explain individual predictions.

![SHAP Waterfall](graphics/output8.png)

---

### Feature Behavior Analysis
SHAP dependence plots confirm interpretable feature–price relationships.

![SHAP Dependence](graphics/output9.png)

---

## Fair Price Range Estimation (Quantile Regression)

### Why Price Ranges Matter
Single-point predictions imply false certainty. Real markets require **price intervals**.

---

### Quantile Regression with CatBoost
Three separate models were trained:

- **25th percentile:** lower bound
- **50th percentile:** recommended price
- **75th percentile:** upper bound

Example output:

Lower bound (25%):        £5,939  
Recommended price (50%): £6,135  
Upper bound (75%):       £6,560  

---

## FastAPI – Price Range Prediction API

The trained models are exposed via a **FastAPI** service that returns a fair price range.

---

### API Access

- **Swagger UI:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

---
---

## Streamlit – Interactive Frontend

An interactive Streamlit application is built on top of the FastAPI backend to allow
users to input vehicle details and instantly receive a fair price range.

The interface communicates directly with the FastAPI `/predict` endpoint and displays
quantile-based pricing results (Q25 / Q50 / Q75) in a clear and user-friendly layout.

---

### Streamlit Interface – Main View

![Streamlit Main Interface](graphics/image2.png)

---

### Streamlit Interface – Result & API Integration

![Streamlit Result View](graphics/image3.png)

---

---

Local Development & Deployment Notes
Local Development (Codespaces / Local Machine)

This project uses FastAPI as a backend service for model inference and Streamlit as a frontend user interface.

During local development, FastAPI and Streamlit are executed as separate processes.

Start FastAPI Backend
python -m uvicorn api_fastapi:app --app-dir fastapi --host 0.0.0.0 --port 8000

Start Streamlit Frontend
streamlit run fastapi/streamlit_app.py


The Streamlit application communicates with the FastAPI backend via HTTP requests.

Deployment Considerations

Running FastAPI and Streamlit within the same container or process is acceptable for:

Local development

Demos

Portfolio projects

Proof-of-concept implementations

For production deployments, it is recommended to deploy FastAPI as an independent service, such as:

Render

Railway

Fly.io

Google Cloud Run

Streamlit should then consume the FastAPI service via a configurable API endpoint.

In cloud environments (e.g. Streamlit Cloud), 127.0.0.1 or localhost must not be used as the API endpoint. Instead, the publicly accessible FastAPI service URL should be provided through environment variables.

API Configuration

The Streamlit application expects the FastAPI base URL to be defined via an environment variable:

API_URL=http://<fastapi-service-url>


This configuration enables seamless switching between local development and cloud deployment environments without modifying the application code.


Technologies Used

Python

Pandas

NumPy

CatBoost

SHAP

FastAPI

Streamlit

Matplotlib / Seaborn

---
