# Olist E-Commerce Analytics: Retention, Churn & Experimentation

## Project Summary
This project is an end-to-end **data analytics case study** on the Olist Brazilian e-commerce dataset.  
The objective is to analyze **customer retention**, evaluate whether **churn can be predicted without data leakage**, and determine **which analytical approaches are most effective for improving repeat purchases**.

The project follows a realistic analytics workflow:  
data preparation → metric definition → modeling → statistical validation → experimentation → business recommendations.

---

## Business Objectives
- Analyze revenue trends over time
- Measure customer retention and repeat purchase behavior
- Define churn correctly using time-based logic
- Evaluate churn prediction under leakage-free conditions
- Validate findings using statistical hypothesis testing
- Demonstrate how A/B testing can guide retention strategy

---

## Dataset
- **Source:** Olist Brazilian E-Commerce Dataset (Kaggle)
- **Time period:** 2016–2018
- **Core tables:** customers, orders, order_items, payments, products
- **Data grain:** order-level and customer-level

Raw datasets are stored in `data/` and treated as immutable inputs.



---

## Repository Structure

olist-analyst-project/
│
├── scripts/ # Executable analysis pipeline
├── output/ # Generated datasets and figures
│ └── figures/ # Final visualizations (PNG)
├── sql/ # SQL queries (reference)
├── data/ # Raw datasets
├── README.md
└── business_recommendations.md


The project is **script-based** (not notebook-based) to ensure reproducibility.

---

## Analysis Pipeline

### 1. Revenue Analysis
**Script:** `scripts/run_analysis.py`  
- Loads transactional data using DuckDB
- Filters delivered orders
- Aggregates monthly revenue

**Output:** `output/monthly_revenue.csv`

---

### 2. Retention & Repeat Purchase Metrics
**Script:** `scripts/run_retention_analysis.py`  
- Calculates orders per customer
- Identifies repeat customers
- Computes repeat purchase rate

**Output:** `output/retention_metrics.csv`

**Finding:**  
Customer retention is very low; the majority of customers purchase only once.

---

### 3. Churn Definition & Feature Engineering
**Script:** `scripts/run_churn_feature_extraction_v2.py`

- Defines churn using inactivity relative to dataset end date
- Avoids future data leakage
- Engineers customer-level features:
  - total_orders  
  - total_revenue  
  - avg_order_value  
  - days_since_last_order  
  - is_churned  

**Output:** `output/churn_features_v2.csv`

---

### 4. Churn Prediction (Leakage-Aware)
**Script:** `scripts/run_churn_logistic_regression_v2.py`

- Logistic regression with proper train/test split
- Feature scaling
- Leakage explicitly removed

**Output:** `output/logistic_regression_coefficients_v2.csv`

**Result:**  
Predictive performance drops significantly without leakage, indicating weak early churn signal in transactional data.

---

### 5. Statistical Hypothesis Testing
**Script:** `scripts/run_churn_statistical_tests.py`

- t-tests and Mann–Whitney tests
- Comparison of churned vs retained customers

**Output:** `output/churn_statistical_tests.csv`

**Result:**  
No statistically significant behavioral differences, supporting the modeling findings.

---

### 6. A/B Testing & Experimentation
**Script:** `scripts/run_ab_test_retention.py`

- Simulated A/B test on first-time customers
- Control vs treatment groups
- Measured second-purchase conversion lift
- Z-test for statistical significance

**Output:** `output/ab_test_second_purchase_results.csv`

**Insight:**  
When prediction is weak, experimentation is a more effective retention strategy.

---

### 7. Visualization
**Script:** `scripts/run_visualizations.py`

Generates business-focused visualizations:
- Monthly revenue trend
- Order frequency distribution (log scale)
- Retention breakdown (one-time vs repeat)
- Churn feature comparison
- Logistic regression coefficient interpretation
- A/B test conversion lift

**Location:** `output/figures/`

---

### 8. Interactive Streamlit Dashboard
**Script:** `app.py`

A comprehensive, interactive dashboard built with Streamlit and Plotly featuring:

- **🏠 Overview Page**: Key KPIs, revenue trends, and retention breakdown
- **📈 Revenue Analysis**: Monthly trends, YoY comparison, growth metrics
- **🔄 Retention & Churn**: Order frequency, churn feature comparison, model performance
- **🧪 A/B Testing**: Conversion rate comparison, statistical significance, lift analysis
- **🔬 Statistical Analysis**: Hypothesis testing results with visualizations
- **📋 Data Explorer**: Browse and download all datasets

**To run the dashboard:**
```bash
pip install streamlit plotly pandas
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`

---

## Key Findings
- ~97% of customers do not make a second purchase
- Early churn is difficult to predict without leakage
- Statistical tests confirm limited behavioral separation
- Controlled experiments provide clearer decision signals than predictive models

---

## Business Recommendations
See `business_recommendations.md` for detailed recommendations, including:
- Focus on post-purchase engagement
- Incentivize second purchase
- Use experimentation to guide retention strategy
- Avoid over-engineering churn models when signal is weak

---

## Tools & Technologies
- SQL (DuckDB / PostgreSQL-style queries)
- Python (pandas, numpy, scikit-learn, scipy)
- Visualization (matplotlib, seaborn)
- Git & GitHub

---

## Reproducibility
All results can be regenerated by executing the scripts in the following order:
1. `run_analysis.py`
2. `run_retention_analysis.py`
3. `run_churn_feature_extraction_v2.py`
4. `run_churn_logistic_regression_v2.py`
5. `run_churn_statistical_tests.py`
6. `run_ab_test_retention.py`
7. `run_visualizations.py`

