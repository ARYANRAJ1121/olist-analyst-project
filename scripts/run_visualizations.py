import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")

os.makedirs(FIG_DIR, exist_ok=True)
sns.set(style="whitegrid")

# =========================
# 1. Monthly Revenue Trend
# =========================
rev = pd.read_csv(os.path.join(OUTPUT_DIR, "monthly_revenue.csv"))
plt.figure(figsize=(10, 5))
plt.plot(rev["month"], rev["revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "01_monthly_revenue.png"))
plt.close()

# =========================
# 2. Order Frequency Distribution (LOG SCALE)
# =========================
churn = pd.read_csv(os.path.join(OUTPUT_DIR, "churn_features_v2.csv"))
plt.figure(figsize=(8, 5))
sns.countplot(x="total_orders", data=churn)
plt.title("Order Frequency Distribution")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")
plt.yscale("log")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "02_order_frequency.png"))
plt.close()

# =========================
# 3. Retention Breakdown
# =========================
ret = pd.read_csv(os.path.join(OUTPUT_DIR, "retention_metrics.csv"))
repeat_rate = ret["repeat_purchase_rate"].iloc[0]
one_time_rate = 1 - repeat_rate

labels = ["One-time Customers", "Repeat Customers"]
values = [one_time_rate * 100, repeat_rate * 100]

plt.figure(figsize=(7, 5))
sns.barplot(x=labels, y=values)
plt.title("Customer Retention Breakdown")
plt.ylabel("Percentage of Customers (%)")
plt.ylim(0, 100)

for i, v in enumerate(values):
    plt.text(i, v + 1, f"{v:.1f}%", ha="center")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "03_retention_breakdown.png"))
plt.close()

# =========================
# 4. Churn Feature Comparison
# =========================
features = ["total_orders", "total_revenue", "avg_order_value"]
plt.figure(figsize=(12, 4))
for i, f in enumerate(features, 1):
    plt.subplot(1, 3, i)
    sns.boxplot(x="is_churned", y=f, data=churn)
    plt.title(f)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "04_churn_feature_comparison.png"))
plt.close()

# =========================
# 5. Logistic Regression Coefficients
# =========================
coef = pd.read_csv(os.path.join(OUTPUT_DIR, "logistic_regression_coefficients_v2.csv"))
plt.figure(figsize=(8, 5))
sns.barplot(x="coefficient", y="feature", data=coef)
plt.title("Logistic Regression Coefficients")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "05_logistic_coefficients.png"))
plt.close()

# =========================
# 6. A/B Test Conversion Lift
# =========================
ab = pd.read_csv(os.path.join(OUTPUT_DIR, "ab_test_second_purchase_results.csv"))
plt.figure(figsize=(6, 5))
sns.barplot(x="group", y="conversion_rate", data=ab)
plt.title("A/B Test: Second Purchase Conversion")
plt.ylabel("Conversion Rate")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "06_ab_test_conversion.png"))
plt.close()

print("All visualizations generated in output/figures/")
