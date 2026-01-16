# Used Car Price Prediction

A machine learning project that predicts used car prices based on vehicle attributes and provides
an explainable pricing recommendation using CatBoost and SHAP.

## Dataset
Combined dataset from multiple brands (processed into a unified schema).

## Features
- model, transmission, fuelType
- mileage, age, engineSize, mpg, tax

## Model
- CatBoostRegressor trained on log(price)
- MAE (test): ~£1,142

## Explainability
- SHAP summary and waterfall plots

## Price Range
- Quantile regression (25% / 50% / 75%) for fair price band estimation

## Project Structure
- `notebooks/eda.ipynb`
- `notebooks/model_training.ipynb`
- `data/processed/used_car_data.csv` (optional)
