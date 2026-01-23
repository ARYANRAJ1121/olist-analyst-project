import pandas as pd
import numpy as np
import os
from scipy.stats import norm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


df = pd.read_csv(os.path.join(DATA_DIR, "churn_features_v2.csv"))


eligible = df[df["total_orders"] == 1].copy()


np.random.seed(42)
eligible["group"] = np.random.choice(
    ["control", "treatment"],
    size=len(eligible),
    p=[0.5, 0.5]
)


baseline_rate = 0.03
treatment_lift = 0.02

eligible["second_purchase"] = np.where(
    eligible["group"] == "control",
    np.random.binomial(1, baseline_rate, len(eligible)),
    np.random.binomial(1, baseline_rate + treatment_lift, len(eligible))
)


summary = eligible.groupby("group")["second_purchase"].agg(
    conversions="sum",
    users="count"
).reset_index()

summary["conversion_rate"] = summary["conversions"] / summary["users"]

print("\nA/B Test Summary:")
print(summary)


c = summary.loc[summary["group"] == "control"].iloc[0]
t = summary.loc[summary["group"] == "treatment"].iloc[0]

p_pool = (c["conversions"] + t["conversions"]) / (c["users"] + t["users"])
se = np.sqrt(p_pool * (1 - p_pool) * (1 / c["users"] + 1 / t["users"]))
z_score = (t["conversion_rate"] - c["conversion_rate"]) / se
p_value = 2 * (1 - norm.cdf(abs(z_score)))

print(f"\nZ-score: {z_score:.3f}")
print(f"P-value: {p_value:.4f}")


summary["z_score"] = z_score
summary["p_value"] = p_value

output_path = os.path.join(OUTPUT_DIR, "ab_test_second_purchase_results.csv")
summary.to_csv(output_path, index=False)

print(f"\nA/B test results saved at: {output_path}")
