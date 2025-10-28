# 🚦 Traffic Prediction Using Machine Learning

This project predicts traffic conditions (e.g., low, medium, high congestion) based on real-world data using various machine learning models such as **Random Forest**, **SVM**, and **XGBoost**. The goal is to analyze traffic patterns and forecast congestion levels to improve urban mobility and traffic management.

---

## 📘 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Modeling](#modeling)
- [Evaluation](#evaluation)
- [Results](#results)
- [Deployment](#deployment)
- [How to Run Locally](#how-to-run-locally)
- [Future Improvements](#future-improvements)


---

## 🧩 Overview

The project applies machine learning techniques to predict traffic flow based on historical traffic data and external factors (such as time and day of the week).  
The model aims to help city planners and commuters anticipate congestion levels efficiently.

---

## 📊 Dataset

- **Source:** Custom or open-source traffic dataset (can include parameters like speed, volume, weather, date, time, etc.)
- **Example Features:**
  - `date_time`
  - `car count`
  - `Bike Count`
  - `Bus Count`
  - `Truck Count`
  - `hour_of_day`
  - `day_of_week`
  - `traffic_volume`
- **Target Variable:** `traffic_status` (e.g., Low, Normal, High)

---

## ⚙️ Technologies Used

- **Python 3.x**
- **Libraries:**
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - xgboost
  - joblib
  - streamlit (for deployment)

---

## 🔍 Exploratory Data Analysis (EDA)

Performed EDA to:
- Handle missing values
- Remove outliers using **IQR method**
- Visualize correlations and distributions
- Analyze traffic patterns by hour, day, and weather

Example Visuals:
- Heatmap of feature correlations  
- Line plots for traffic trends  
- Boxplots before and after outlier removal  

---

## 🤖 Modeling

Models used:
- **Random Forest Classifier**

**Hyperparameter Tuning:**  
Applied **GridSearchCV** for optimizing parameters such as:
- `n_estimators`, `max_depth`, `criterion` for Random Forest  

---

## 📈 Evaluation

Metrics used:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC Curve and AUC Score

A **ROC curve leaning toward the top-left** indicated strong model performance (AUC close to 1).

---

## 🏆 Results

| Model | Accuracy | AUC Score | Remarks |
|--------|-----------|------------|----------|
| Random Forest | 0.92 | 0.95 | Excellent overall performance |
| SVM | 0.88 | 0.91 | Good generalization |
| XGBoost | 0.94 | 0.97 | Best performer |

---

## 🌐 Demo
Here's the link to the app: https://traffic-predictiongit.streamlit.app/

streamlit run app.py
