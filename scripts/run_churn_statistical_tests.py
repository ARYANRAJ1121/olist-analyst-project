
import pandas as pd
import numpy as np
import os
from scipy.stats import ttest_ind, mannwhitneyu


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "output")


df = pd.read_csv(os.path.join(DATA_DIR, "churn_features_v2.csv"))


churned = df[df["is_churned"] == 1]
active = df[df["is_churned"] == 0]

features = ["total_orders", "total_revenue", "avg_order_value"]

results = []


for feature in features:
    x1 = churned[feature].dropna()
    x0 = active[feature].dropna()

    t_stat, t_p = ttest_ind(x1, x0, equal_var=False)

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


output_path = os.path.join(DATA_DIR, "churn_statistical_tests.csv")
results_df.to_csv(output_path, index=False)

print(f"\nStatistical test results saved at: {output_path}")
