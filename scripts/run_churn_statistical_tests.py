# scripts/run_churn_statistical_tests.py

import pandas as pd
import numpy as np
import os
from scipy.stats import ttest_ind, mannwhitneyu

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
# SPLIT GROUPS
# =============================
churned = df[df["is_churned"] == 1]
active = df[df["is_churned"] == 0]

features = ["total_orders", "total_revenue", "avg_order_value"]

results = []

# =============================
# STATISTICAL TESTS
# =============================
for feature in features:
    x1 = churned[feature].dropna()
    x0 = active[feature].dropna()

    # Welch's t-test
    t_stat, t_p = ttest_ind(x1, x0, equal_var=False)

    # Mann–Whitney U test
    u_stat, u_p = mannwhitneyu(x1, x0, alternative="two-sided")

    results.append({
        "feature": feature,
        "churned_mean": x1.mean(),
        "active_mean": x0.mean(),
        "t_test_p_value": t_p,
        "mannwhitney_p_value": u_p
    })

results_df = pd.DataFrame(results)

print("\nStatistical Test Results:")
print(results_df)

# =============================
# SAVE OUTPUT
# =============================
output_path = os.path.join(DATA_DIR, "churn_statistical_tests.csv")
results_df.to_csv(output_path, index=False)

print(f"\nStatistical test results saved at: {output_path}")
