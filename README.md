# Used Car Price Prediction & Fair Pricing System

This project focuses on predicting used car prices based on vehicle characteristics and providing
**transparent and actionable pricing recommendations** for sellers.  
Instead of producing a single point estimate, the system predicts a **fair price range** using
quantile regression and explains predictions using **SHAP**.

---

##  Motivation

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
Used car prices are heavily right-skewed, with most vehicles concentrated in lower price ranges and
a long tail of expensive cars.

![Price Distribution](graphics/output.png)

---

### Log-Transformed Price Distribution
To reduce skewness and stabilize variance, prices were log-transformed before modeling.

![Log Price Distribution](graphics/output1.png)

---

### Vehicle Age vs Price
Vehicle prices decrease as age increases, showing a strong negative and nonlinear relationship.

![Age vs Price](graphics/output2.png)

---

### Mileage vs Price
Higher mileage is clearly associated with lower prices, particularly beyond high mileage levels.

![Mileage vs Price](graphics/output3.png)

---

### Price Distribution by Fuel Type
Fuel type influences price distribution, with electric and hybrid vehicles generally exhibiting
higher median prices.

![Fuel Type vs Price](graphics/output4.png)

---

### Price Distribution by Transmission Type
Automatic and semi-automatic vehicles tend to have higher prices compared to manual vehicles.

![Transmission vs Price](graphics/output5.png)

---

### Engine Size vs Price
Larger engine sizes are generally associated with higher prices, though variance increases for
higher displacements.

![Engine Size vs Price](graphics/output6.png)

---

## Model Training

### Model Choice
- **CatBoostRegressor**
- Native handling of categorical variables
- Strong performance on tabular datasets
- Robust to nonlinear feature interactions

The target variable was modeled as **log(price)**.

---

### Model Performance
- **Test MAE:** approximately **£1,142**

This error level is acceptable in the used car market, where negotiation and seller behavior
introduce natural variability.

---

## Model Explainability with SHAP

### Global Feature Importance
The SHAP summary plot highlights which features most strongly influence price predictions.

![SHAP Summary](graphics/output7.png)

**Key drivers identified by SHAP:**
- Vehicle model  
- Vehicle age  
- Engine size  
- Mileage  

These factors align well with real-world vehicle pricing logic.

---

### Local Explanation (Single Vehicle)
SHAP waterfall plots explain individual predictions by showing how each feature shifts the price
relative to the model’s baseline.

![SHAP Waterfall](graphics/output8.png)

This allows answering the question:  
> *Why did the model recommend this price for this specific vehicle?*

---

### Feature Behavior Analysis
SHAP dependence plots confirm consistent and interpretable relationships between features and
predicted prices.

![SHAP Dependence Plot](graphics/output9.png)

---

## Fair Price Range Estimation (Quantile Regression)

### Why Price Ranges Matter
A single predicted price implies false certainty.  
In real markets, sellers benefit from understanding a **reasonable price interval** rather than
a fixed value.

---

### Quantile Regression with CatBoost
Three separate models were trained to estimate different parts of the price distribution:

- **25th percentile:** lower bound (quick sale scenario)  
- **50th percentile:** recommended price  
- **75th percentile:** upper bound (optimistic pricing scenario)  

#### Example Output (Single Vehicle)

Lower bound (25%):        £5,939
Recommended price (50%): £6,135
Upper bound (75%):       £6,560
True price:              £5,800

The true selling price falls very close to the lower bound, indicating a faster-sale or negotiated
pricing scenario.

---

## Key Takeaways

- The model captures realistic used car pricing behavior  
- Predictions are explainable at both global and individual levels  
- Quantile-based price ranges provide actionable guidance for sellers  
- The system is suitable for real-world deployment  

---

## Next Steps

- Build an interactive pricing interface using **Streamlit**
- Expose prediction functionality via **FastAPI**
- Allow users to input custom vehicle details
- Provide real-time pricing recommendations

---

## Technologies Used

- Python  
- Pandas, NumPy  
- CatBoost  
- SHAP  
- Matplotlib / Seaborn  
