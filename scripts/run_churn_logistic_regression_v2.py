import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.impute import SimpleImputer

# =============================
# PATH SETUP
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "output")

# =============================
# LOAD DATA
# =============================
df = pd.read_csv(os.path.join(DATA_DIR, "churn_features_v2.csv"))

# =============================
# LEAKAGE-FREE FEATURES
# (NO recency / days_since_last_order)
# =============================
features = [
    "total_orders",
    "total_revenue",
    "avg_order_value"
]

X = df[features]
y = df["is_churned"]

# =============================
# HANDLE MISSING VALUES
# =============================
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

# =============================
# TRAIN TEST SPLIT
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# =============================
# SCALING
# =============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =============================
# LOGISTIC REGRESSION
# =============================
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# =============================
# EVALUATION
# =============================
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

roc_auc = roc_auc_score(y_test, y_prob)
print(f"\nROC-AUC Score: {roc_auc:.3f}")

# =============================
# COEFFICIENT INTERPRETATION
# =============================
coef_df = pd.DataFrame({
    "feature": features,
    "coefficient": model.coef_[0]
}).sort_values(by="coefficient", ascending=False)

print("\nLeakage-Free Logistic Regression Coefficients:")
print(coef_df)

# =============================
# SAVE OUTPUT
# =============================
coef_df.to_csv(
    os.path.join(DATA_DIR, "logistic_regression_coefficients_v2.csv"),
    index=False
)

print("\nLeakage-free model coefficients saved.")
