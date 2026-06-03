############################################Data Preparation (Data Cleaning)############################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv(r"D:\Thesis\4-Dataset\Loan_approval_data_2025.csv")

from sklearn.preprocessing import StandardScaler

############################################correlation analysis with oroginal features without scaled and binary and log tranformed features
num_df = df.select_dtypes(include=[np.number]).copy()
corr_spearman = num_df.corr(method='spearman')

# Focus on correlation with the target
target_corr = corr_spearman['loan_status'].sort_values(ascending=False)
# Visualize this subset
plt.figure(figsize=(6, 8))
sns.barplot(x=target_corr.values, y=target_corr.index, hue=target_corr.index, palette='viridis', legend=False)
plt.title("Feature Correlation with Loan Status befor tranformed features")
plt.show()
print("Correlation Matrix-corr_spearman:")
print(corr_spearman)

mask = np.triu(np.ones_like(corr_spearman, dtype=bool))
plt.figure(figsize=(12, 10))
sns.heatmap(corr_spearman, mask=mask, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Cleaned Correlation Heatmap befor tranformed features")
plt.show()

#######################################################################
############################################correlation analysis with scaled and binary and log tranformed features

# -----------------------------
# Build transformed feature set
# -----------------------------
df_work = df.copy()

# Safe log transforms (handle zeros)
for col in ["current_debt", "annual_income", "savings_assets"]:
    if col in df_work.columns:
        df_work[f"{col}_log"] = np.log1p(df_work[col])

# Scale continuous features (StandardScaler-like without fitting state)
def standardize(series: pd.Series):
    s = series.astype(float)
    return (s - s.mean()) / (s.std(ddof=0) + 1e-12)

scale_cols = {
    "loan_amount": "loan_amount_scaled",
    "credit_history_years": "credit_history_years_scaled",
    "debt_to_income_ratio": "debt_to_income_ratio_scaled",
    "age": "age_scaled",
    "payment_to_income_ratio": "payment_to_income_ratio_scaled",
    "loan_to_income_ratio": "loan_to_income_ratio_scaled",
    "credit_score": "credit_score_scaled",
    "interest_rate": "interest_rate_scaled",
}
for src, dst in scale_cols.items():
    if src in df_work.columns:
        df_work[dst] = standardize(df_work[src])

# Binary features
if "delinquencies_last_2yrs" in df_work.columns:
    df_work["delinquencies_last_2yrs_binary"] = (df_work["delinquencies_last_2yrs"].fillna(0) > 0).astype(int)
if "derogatory_marks" in df_work.columns:
    df_work["derogatory_marks_binary"] = (df_work["derogatory_marks"].fillna(0) > 0).astype(int)

# Years employed log
if "years_employed" in df_work.columns:
    df_work["years_employed_log"] = np.log1p(df_work["years_employed"])

# Keep defaults_on_file as is (assumed binary/integer)
# Ensure loan_status exists and is numeric/binary
assert "loan_status" in df_work.columns, "loan_status column is required"

# ---------------------------------------------------
# Select only the requested engineered feature columns
# ---------------------------------------------------
requested_features = [
    "years_employed_log",
    "current_debt_log",
    "loan_amount_scaled",
    "annual_income_log",
    "credit_history_years_scaled",
    "savings_assets_log",
    "debt_to_income_ratio_scaled",
    "age_scaled",
    "payment_to_income_ratio_scaled",
    "credit_score_scaled",
    "delinquencies_last_2yrs_binary",
    "interest_rate_scaled",
    "derogatory_marks_binary",
    "loan_to_income_ratio_scaled",
    "defaults_on_file",
    "loan_status",  # include target for correlation
]
available_features = [f for f in requested_features if f in df_work.columns]
df_feat = df_work[available_features].copy()

# --------------------------------
# Spearman correlation and plotting
# --------------------------------
num_df = df_feat.select_dtypes(include=[np.number]).copy()
corr_spearman = num_df.corr(method='spearman')

target_corr = corr_spearman['loan_status'].drop(labels=['loan_status']).sort_values(ascending=False)

plt.figure(figsize=(7, max(4, 0.4 * len(target_corr))))
sns.barplot(x=target_corr.values, y=target_corr.index, palette='viridis')
plt.title("Feature Spearman Correlation with Loan Status after tranformed features")
plt.xlabel("Spearman ρ")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

print("Spearman Correlation Matrix (selected engineered features after tranformed features):")
print(corr_spearman)

mask = np.triu(np.ones_like(corr_spearman, dtype=bool))
plt.figure(figsize=(12, 10))
sns.heatmap(corr_spearman, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", cbar_kws={'label': 'Spearman ρ'})
plt.title("Engineered Feature Correlation Heatmap (Spearman) after tranformed features")
plt.tight_layout()
plt.show()













