############################################Data Preparation (Data Cleaning)############################################
import pandas as pd
import os

############################################ 1 - Load the original dataset

df = pd.read_csv(r"D:\Thesis\4-Dataset\Loan_approval_data_2025.csv",sep=',' , encoding="utf-8")
print(df.columns)
print(df.head(20))
print(df.tail(20))
print(df.shape)

 ############################################ 2- Checking corrupted rows
import re

corrupted_rows = []
df['loan_status'] = df['loan_status'].astype(int)

# Business rule validations
for idx, row in df.iterrows():
    issues = []
    
    # Age validation (18-100)
    if pd.notna(row['age']) and (row['age'] < 18 or row['age'] > 100):
        issues.append('Invalid age')
    
    # Credit score validation (300-850)
    if pd.notna(row['credit_score']) and (row['credit_score'] < 300 or row['credit_score'] > 850):
        issues.append('Invalid credit_score')
    
    # Years employed validation (0-60)
    if pd.notna(row['years_employed']) and (row['years_employed'] < 0 or row['years_employed'] > 60):
        issues.append('Invalid years_employed')
    
    # Credit history years validation (0-80)
    if pd.notna(row['credit_history_years']) and (row['credit_history_years'] < 0 or row['credit_history_years'] > 80):
        issues.append('Invalid credit_history_years')
    
    # Negative values validation
    if pd.notna(row['annual_income']) and row['annual_income'] < 0:
        issues.append('Negative annual_income')
    if pd.notna(row['savings_assets']) and row['savings_assets'] < 0:
        issues.append('Negative savings_assets')
    if pd.notna(row['current_debt']) and row['current_debt'] < 0:
        issues.append('Negative current_debt')
    if pd.notna(row['loan_amount']) and row['loan_amount'] < 0:
        issues.append('Negative loan_amount')
    
    # Interest rate validation (0-100%)
    if pd.notna(row['interest_rate']) and (row['interest_rate'] < 0 or row['interest_rate'] > 100):
        issues.append('Invalid interest_rate')
    
    # Ratio validations (0-100)
    if pd.notna(row['debt_to_income_ratio']) and (row['debt_to_income_ratio'] < 0 or row['debt_to_income_ratio'] > 100):
        issues.append('Invalid debt_to_income_ratio')
    if pd.notna(row['loan_to_income_ratio']) and (row['loan_to_income_ratio'] < 0 or row['loan_to_income_ratio'] > 100):
        issues.append('Invalid loan_to_income_ratio')
    if pd.notna(row['payment_to_income_ratio']) and (row['payment_to_income_ratio'] < 0 or row['payment_to_income_ratio'] > 100):
        issues.append('Invalid payment_to_income_ratio')
    
    # Defaults and delinquencies validation (non-negative)
    if pd.notna(row['defaults_on_file']) and row['defaults_on_file'] < 0:
        issues.append('Negative defaults_on_file')
    if pd.notna(row['delinquencies_last_2yrs']) and row['delinquencies_last_2yrs'] < 0:
        issues.append('Negative delinquencies_last_2yrs')
    if pd.notna(row['derogatory_marks']) and row['derogatory_marks'] < 0:
        issues.append('Negative derogatory_marks')
    
    # String field validation using regex
    if pd.notna(row['occupation_status']):
        if not re.match(r'^[A-Za-z\s\-]+$', str(row['occupation_status'])):
            issues.append('Malformed occupation_status')
    
    if pd.notna(row['product_type']):
        if not re.match(r'^[A-Za-z\s\-]+$', str(row['product_type'])):
            issues.append('Malformed product_type')
    
    if pd.notna(row['loan_status']):
       if int(row['loan_status']) not in [0, 1]:
           issues.append('Malformed loan_status')

    
    # Logical inconsistencies
    if pd.notna(row['credit_history_years']) and pd.notna(row['age']):
        if row['credit_history_years'] > row['age'] - 18:
            issues.append('Credit history exceeds possible years')
    
    if pd.notna(row['years_employed']) and pd.notna(row['age']):
        if row['years_employed'] > row['age'] - 18:
            issues.append('Years employed exceeds possible years')
    
    # Missing critical values
    if pd.isna(row['customer_id']) or pd.isna(row['loan_status']):
        issues.append('Missing critical field')
    
    if issues:
        corrupted_rows.append({
            'index': idx,
            'customer_id': row['customer_id'],
            'issues': ', '.join(issues),
            'row_data': row
        })

# Display results
print(f"Total corrupted rows found: {len(corrupted_rows)}\n")

for corrupt in corrupted_rows:
    print(f"Row Index: {corrupt['index']}")
    print(f"Customer ID: {corrupt['customer_id']}")
    print(f"Issues: {corrupt['issues']}")
    print(f"Data: {corrupt['row_data'].to_dict()}")
    print("-" * 80)

#################### we found 144 rows that loan_to_income_ratio & debt_to_income_ratio have inproper ratio so:

# Remove rows where annual_income is missing or zero
df = df[df['annual_income'].notna()]
df = df[df['annual_income'] > 0]

# Recalculate ratios
df['loan_to_income_ratio'] = df['loan_amount'] / df['annual_income']
df['debt_to_income_ratio'] = df['current_debt'] / df['annual_income']

# Remove first row if needed
df_corrected = df.iloc[1:].copy()


# Save dataset
df_corrected.to_csv(r"D:\Thesis\4-Dataset\Loan_approval_data_2025-1.csv", index=False)

print("✅ New corrected dataset saved as Loan_approval_data_2025-1.csv")

df = pd.read_csv(r"D:\Thesis\4-Dataset\Loan_approval_data_2025-1.csv")

###########################################################
############################################ 3-Checking Column Types Fix column data types
df["age"] = df["age"].astype(int)
df["defaults_on_file"] = df["defaults_on_file"].astype(int)
df["delinquencies_last_2yrs"] = df["delinquencies_last_2yrs"].astype(int)
df["derogatory_marks"] = df["derogatory_marks"].astype(int)
df["loan_status"] = df["loan_status"].astype(int)


############################################ 4-handle missing value
print(df.isna().sum(axis=1))

############################################ 5-normalize inconsistent text (“Male” vs “male”) in rows
print(df["occupation_status"].value_counts())
print(df["product_type"].value_counts())
print(df["loan_intent"].value_counts())

############################################ 6- recognizing missing value
print(df.isna().sum())

############################################ 7- Preprocessing: Handle missing values if necessary
df.dropna(inplace=True)      # Example: remove rows with missing values

 ############################################ 8-Cheking Duplicated row
duplicates_count = df.duplicated().sum()
# Check if there are any duplicate rows and print the result using f-strings
if df.duplicated().any():
    print(f"Duplicates are present. Total duplicate rows: {duplicates_count}")
    df = df.drop_duplicates()
    print("Duplicates values is deleted")
else:
    print(f"No duplicates are present in the Dataset.")


############################################Exploratory Data Analysis (EDA)##############################
############################################ 1-Statistical Summaries 
print(df.describe(include='object'))
print(df.nunique())

pd.set_option('display.max_columns', None)
print(df.describe())

############################################ 2-plot distributions and histograms
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
df.hist(figsize=(15,15), bins=30)
plt.tight_layout()
plt.show()

print(df['years_employed'].skew())   #skew=1.29 so we use log-transform
df["years_employed_log"] = np.log1p(df["years_employed"])   
sns.histplot(df["years_employed_log"], kde=True)
plt.show()
print("Skew after:", df["years_employed_log"].skew()) #Skew after log-transform: -0.103
print(df['years_employed_log'].describe()) # max=3.7 is , mean=1.69 
Q1 = df['years_employed_log'].quantile(0.25)   # identifying outlier
Q3 = df['years_employed_log'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['years_employed_log'] < lower_bound) | (df['years_employed_log'] > upper_bound)]
print("Number of outliers:", len(outliers)) #Number of outliers: from 1373 to 0

print(df['current_debt'].skew())   #skew=2.43 so we use log-transform
df["current_debt_log"] = np.log1p(df["current_debt"])   
sns.histplot(df["current_debt_log"], kde=True)
plt.show()
print("Skew after:", df["current_debt_log"].skew()) #Skew after log-transform: -0.451
print(df['current_debt_log'].describe()) # max=12 , mean=9
Q1 = df['current_debt_log'].quantile(0.25)   # identifying outlier
Q3 = df['current_debt_log'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['current_debt_log'] < lower_bound) | (df['current_debt_log'] > upper_bound)]
print("Number of outliers:", len(outliers)) #Number of outliers: from 2932 to 638

################start-->loan_amount
from sklearn.preprocessing import StandardScaler
print(df['loan_amount'].skew())   #skew=0.93 so we use StandardScaler  
print(df['loan_amount'].describe()) # max=100000 is extremly biger than mean=33041 so for making sure i use IQR to be confident whether we have outlier or not
scaler = StandardScaler()             #StandardScaler
df['loan_amount_scaled'] = scaler.fit_transform(df[['loan_amount']])
Q1 = df['loan_amount_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['loan_amount_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['loan_amount_scaled'] < lower_bound) | (df['loan_amount_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers)) #Number of outliers: 0 so we do not need to do anything
################end-->loan_amount

print(df['annual_income'].skew())    #skew=1.88 so we use log-transform
df["annual_income_log"] = np.log1p(df["annual_income"])
sns.histplot(df["annual_income_log"], kde=True)
plt.show()
print("Skew after:", df["annual_income_log"].skew()) #Skew after log-transform: -0.18
Q1 = df['annual_income_log'].quantile(0.25)   # identifying outlier
Q3 = df['annual_income_log'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['annual_income_log'] < lower_bound) | (df['annual_income_log'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: from 2355 sto 123


print(df['credit_history_years'].skew()) #skew=0.95 so we use StandardScaler  
print(df['credit_history_years'].describe()) # max=30 is extremly biger than mean=83595 
scaler = StandardScaler()             #StandardScaler
df['credit_history_years_scaled'] = scaler.fit_transform(df[['credit_history_years']])
Q1 = df['credit_history_years_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['credit_history_years_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['credit_history_years_scaled'] < lower_bound) | (df['credit_history_years_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 349 so we need to remove them


print(df['savings_assets'].skew())                   #skew=12.1 so we use log-transform
print(df['savings_assets'].describe()) # max=300000 is extremly biger than mean=3595 so we have outlier in this feature--> removing Outlier 
df["savings_assets_log"] = np.log1p(df["savings_assets"])
sns.histplot(df["savings_assets_log"], kde=True)
plt.show()
print("Skew after:", df["savings_assets_log"].skew()) #Skew after log-transform: -0.24
Q1 = df['savings_assets_log'].quantile(0.25)   # identifying outlier
Q3 = df['savings_assets_log'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['savings_assets_log'] < lower_bound) | (df['savings_assets_log'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: from 6508 to 509

print(df['debt_to_income_ratio'].skew())   #skew=0.44 so we use StandardScaler  
print(df['debt_to_income_ratio'].describe()) # max=799 , mean=256
scaler = StandardScaler()             #StandardScaler
df['debt_to_income_ratio_scaled'] = scaler.fit_transform(df[['debt_to_income_ratio']])
Q1 = df['debt_to_income_ratio_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['debt_to_income_ratio_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['debt_to_income_ratio_scaled'] < lower_bound) | (df['debt_to_income_ratio_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 174

print(df['loan_to_income_ratio'].skew())   #skew=0.64 so we use StandardScaler  
print(df['loan_to_income_ratio'].describe()) # max=2001 , mean=622 
scaler = StandardScaler()             #StanardScalerd
df['loan_to_income_ratio_scaled'] = scaler.fit_transform(df[['loan_to_income_ratio']])
Q1 = df['loan_to_income_ratio_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['loan_to_income_ratio_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['loan_to_income_ratio_scaled'] < lower_bound) | (df['loan_to_income_ratio_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 0 

print(df['age'].skew())   #skew=0.335  
print(df['age'].describe()) #max=70 , mean=34 , median=35
scaler = StandardScaler()   #StandardScaler
df['age_scaled'] = scaler.fit_transform(df[['age']])
Q1 = df['age_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['age_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['age_scaled'] < lower_bound) | (df['age_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 112 

print(df['payment_to_income_ratio'].skew())   #skew=0.65  
print(df['payment_to_income_ratio'].describe()) #max=667 , mean=210 , median=184
scaler = StandardScaler()   #StandardScaler
df['payment_to_income_ratio_scaled'] = scaler.fit_transform(df[['payment_to_income_ratio']])
Q1 = df['payment_to_income_ratio_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['payment_to_income_ratio_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['payment_to_income_ratio_scaled'] < lower_bound) | (df['payment_to_income_ratio_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 0 

from sklearn.preprocessing import StandardScaler
print(df['loan_to_income_ratio'].skew())   #skew=0.64 
print(df['loan_to_income_ratio'].describe()) #max=2001 , mean=622 , median=547
scaler = StandardScaler()   #StandardScaler
df['loan_to_income_ratio_scaled'] = scaler.fit_transform(df[['loan_to_income_ratio']])
Q1 = df['loan_to_income_ratio_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['loan_to_income_ratio_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['loan_to_income_ratio_scaled'] < lower_bound) | (df['loan_to_income_ratio_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 0 


print(df['credit_score'].skew())   #skew=0.012 
print(df['credit_score'].describe()) #max=850 , mean=643 , median=643
scaler = StandardScaler()   #StandardScaler
df['credit_score_scaled'] = scaler.fit_transform(df[['credit_score']])
Q1 = df['credit_score_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['credit_score_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['credit_score_scaled'] < lower_bound) | (df['credit_score_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 349 

print(df['delinquencies_last_2yrs'].skew())   #skew=1.8 
print(df['delinquencies_last_2yrs'].describe()) #max=9 , mean=0.554 , median=0
sns.histplot(df['delinquencies_last_2yrs'], kde=False, bins=10)
plt.title('Delinquencies in the Last 2 Years - Distribution')
plt.show()
df['delinquencies_last_2yrs_binary'] = (df['delinquencies_last_2yrs'] > 0).astype(int)
Q1 = df['delinquencies_last_2yrs_binary'].quantile(0.25)   # identifying outlier
Q3 = df['delinquencies_last_2yrs_binary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['delinquencies_last_2yrs_binary'] < lower_bound) | (df['delinquencies_last_2yrs_binary'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: from 1761 to 0

print(df['interest_rate'].skew())   #skew=0.0196 
print(df['interest_rate'].describe()) #max=23 , mean=15.4 , median=15.44
sns.histplot(df['interest_rate'], kde=False, bins=10)
plt.title('interest_rate - Distribution')
plt.show()
scaler = StandardScaler()
df['interest_rate_scaled'] = scaler.fit_transform(df[['interest_rate']])
Q1 = df['interest_rate_scaled'].quantile(0.25)   # identifying outlier
Q3 = df['interest_rate_scaled'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['interest_rate_scaled'] < lower_bound) | (df['interest_rate_scaled'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 0

print(df['derogatory_marks'].skew())   #skew=3.1 
print(df['derogatory_marks'].describe()) #max=4 , mean=0.147 , median=0
sns.histplot(df['derogatory_marks'], kde=False, bins=10)
plt.title('derogatory_marks - Distribution')
plt.show()
df['derogatory_marks_binary'] = (df['derogatory_marks'] > 0).astype(int) # because we are using descrete feature so we have to convert this feature to binary
Q1 = df['derogatory_marks_binary'].quantile(0.25)   # identifying outlier
Q3 = df['derogatory_marks_binary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['derogatory_marks_binary'] < lower_bound) | (df['derogatory_marks_binary'] > upper_bound)]
print("Number of outliers:", len(outliers))   #Number of outliers: 0--at binary feature having outlier is not make sense because we have just 0 and 1


###############################################################################3-correlation analysis
########correlation analysis with oroginal features without scaled and binary and log tranformed features
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
########correlation analysis with scaled and binary and log tranformed features

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

##############################################4-class imbalance Checking
# Assume target column is 'loan_status'
class_counts = df['loan_status'].value_counts()
class_percent = df['loan_status'].value_counts(normalize=True) * 100
print("Class counts:")
print(class_counts)
print("\nClass percentages:")
print(class_percent)

# Bar plot
sns.countplot(x='loan_status', data=df)
plt.title('Class Distribution')
plt.xlabel('Classes')
plt.ylabel('Count')
plt.show()

df['loan_status'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Class Distribution')
plt.ylabel('')
plt.show()

majority_class_count = class_counts.max()
minority_class_count = class_counts.min()
imbalance_ratio = majority_class_count / minority_class_count
print(f'Imbalance Ratio: {imbalance_ratio:.2f}') ############IR is 1.2 so we need to use class weighting

############################################ 5-Modality
# List of the features you want to plot
features = [
    'years_employed',
    'current_debt',
    'loan_amount',
    'annual_income',
    'credit_history_years',
    'savings_assets',
    'age',
    'credit_score',
    'interest_rate'
]

# Plot each feature
for col in features:
    if col in df.columns:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], kde=True)
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()
    else:
        print(f"Column '{col}' not found in dataframe.")#among our features , only loan_amount is Multimodality so we have to categorize it to three diffrent groups

############################################Feature Engineering##############################
############################################ 1-one‑hot encoding(converting categorial features)
# columns to one-hot encode
df = pd.get_dummies(
    df,
    columns=["occupation_status", "product_type", "loan_intent"],
    dtype=int
)

print(df.columns.tolist())
print(len(df.columns)) #total we have 43 features so we have to pich up which features should use for ML
#['customer_id', 'age', 'years_employed', 'annual_income', 'credit_score', 'credit_history_years',
#  'savings_assets', 'current_debt', 'defaults_on_file', 'delinquencies_last_2yrs',
#  'derogatory_marks', 'loan_amount', 'interest_rate', 'debt_to_income_ratio', 'loan_to_income_ratio',
#  'payment_to_income_ratio', 'loan_status', 'years_employed_log', 'current_debt_log', 'loan_amount_scaled',
#  'annual_income_log', 'credit_history_years_scaled', 'savings_assets_log', 'debt_to_income_ratio_scaled',
#  'loan_to_income_ratio_scaled', 'age_scaled', 'payment_to_income_ratio_scaled', 'credit_score_scaled',
#  'delinquencies_last_2yrs_binary', 'interest_rate_scaled', 'derogatory_marks_binary', 'occupation_status_Employed',
#  'occupation_status_Self-Employed', 'occupation_status_Student', 'product_type_Credit Card', 'product_type_Line of Credit', 
# 'product_type_Personal Loan', 'loan_intent_Business', 'loan_intent_Debt Consolidation', 'loan_intent_Education', 
# 'loan_intent_Home Improvement', 'loan_intent_Medical', 'loan_intent_Personal']

#########recognizing important features##################################### 1- XGBoost to select importance features 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

# -------------------------------------------------------
# 1. Select only engineered + one-hot features
# -------------------------------------------------------
selected_features = [
    'years_employed_log',
    'current_debt_log',
    'loan_amount_scaled',
    'annual_income_log',
    'credit_history_years_scaled',
    'savings_assets_log',
    'debt_to_income_ratio_scaled',
    'loan_to_income_ratio_scaled',
    'age_scaled',
    'payment_to_income_ratio_scaled',
    'credit_score_scaled',
    'interest_rate_scaled',
    'delinquencies_last_2yrs_binary',
    'derogatory_marks_binary',
    'defaults_on_file',

    # one-hot
    'occupation_status_Employed',
    'occupation_status_Self-Employed',
    'occupation_status_Student',

    'product_type_Credit Card',
    'product_type_Line of Credit',
    'product_type_Personal Loan',

    'loan_intent_Business',
    'loan_intent_Debt Consolidation',
    'loan_intent_Education',
    'loan_intent_Home Improvement',
    'loan_intent_Medical',
    'loan_intent_Personal'
]

X = df[selected_features]
y = df["loan_status"]

# -------------------------------------------------------
# 2. Train/test split
# -------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------------------------------
# 3. Train XGBoost model
# -------------------------------------------------------
model = XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

print("XGBoost model trained successfully!")

# -------------------------------------------------------
# 4. Feature Importance Extraction
# -------------------------------------------------------
importance_values = model.feature_importances_
feature_names = X.columns

importance_series = pd.Series(importance_values, index=feature_names)
importance_series = importance_series.sort_values(ascending=False)

print("\n=== XGBoost Feature Importance (sorted) ===")
print(importance_series)

# -------------------------------------------------------
# 5. Plot Feature Importance
# -------------------------------------------------------
plt.figure(figsize=(14, 7))
importance_series.plot(kind='bar')
plt.title("XGBoost Feature Importance (Engineered Features Only)")
plt.ylabel("Importance Score")
plt.xlabel("Feature Name")
plt.tight_layout()
plt.show()

# -------------------------------------------------------
# 6. Identify weak features
# -------------------------------------------------------
threshold = 0.01
low_importance = importance_series[importance_series < threshold]

print("\n=== Features recommended for removal (importance < 0.01) ===")
print(low_importance)


##################################### 2- Permutation Importance to select importance features
#############################################
# 2- Permutation Importance (using selected_features)
#############################################

from sklearn.inspection import permutation_importance
import pandas as pd
import matplotlib.pyplot as plt

# Ensure X and y use your selected engineered features
selected_features = [
    'years_employed_log',
    'current_debt_log',
    'loan_amount_scaled',
    'annual_income_log',
    'credit_history_years_scaled',
    'savings_assets_log',
    'debt_to_income_ratio_scaled',
    'loan_to_income_ratio_scaled',
    'age_scaled',
    'payment_to_income_ratio_scaled',
    'credit_score_scaled',
    'interest_rate_scaled',
    'delinquencies_last_2yrs_binary',
    'derogatory_marks_binary',
    'defaults_on_file',

    # one-hot
    'occupation_status_Employed',
    'occupation_status_Self-Employed',
    'occupation_status_Student',

    'product_type_Credit Card',
    'product_type_Line of Credit',
    'product_type_Personal Loan',

    'loan_intent_Business',
    'loan_intent_Debt Consolidation',
    'loan_intent_Education',
    'loan_intent_Home Improvement',
    'loan_intent_Medical',
    'loan_intent_Personal'
]

X = df[selected_features]
y = df["loan_status"]

# Calculate permutation importance
perm_result = permutation_importance(
    model, X_test, y_test, n_repeats=10, random_state=42
)

perm_importances = pd.Series(
    perm_result.importances_mean,
    index=X.columns
).sort_values(ascending=False)

print("\n=== Permutation Importance ===")
print(perm_importances)

# Plot
plt.figure(figsize=(12, 4))
perm_importances.plot(kind='bar')
plt.title("Permutation Importance (Using Selected Features)")
plt.ylabel("Importance Score")
plt.tight_layout()
plt.show()

##################################### 3- SHAP Values to select importance features
#############################################
# SHAP Values for Selected Features
#############################################

import shap
import pandas as pd

# Use your selected engineered features
selected_features = [
    'years_employed_log',
    'current_debt_log',
    'loan_amount_scaled',
    'annual_income_log',
    'credit_history_years_scaled',
    'savings_assets_log',
    'debt_to_income_ratio_scaled',
    'loan_to_income_ratio_scaled',
    'age_scaled',
    'payment_to_income_ratio_scaled',
    'credit_score_scaled',
    'interest_rate_scaled',
    'delinquencies_last_2yrs_binary',
    'derogatory_marks_binary',
    'defaults_on_file',

    'occupation_status_Employed',
    'occupation_status_Self-Employed',
    'occupation_status_Student',

    'product_type_Credit Card',
    'product_type_Line of Credit',
    'product_type_Personal Loan',

    'loan_intent_Business',
    'loan_intent_Debt Consolidation',
    'loan_intent_Education',
    'loan_intent_Home Improvement',
    'loan_intent_Medical',
    'loan_intent_Personal'
]

X = df[selected_features]
y = df["loan_status"]

# SHAP Explainer
explainer = shap.TreeExplainer(model)

# SHAP Values on the same X_test used for evaluation
shap_values = explainer.shap_values(X_test)

print("Generating SHAP plots...")

# Summary scatter plot
shap.summary_plot(shap_values, X_test)

# Summary bar chart
shap.summary_plot(shap_values, X_test, plot_type="bar")

###################################################
# PRINT GLOBAL SHAP IMPORTANCE VALUES (sorted)
###################################################
shap_importance = pd.DataFrame({
    "feature": X_test.columns,
    "importance": np.abs(shap_values).mean(axis=0)
}).sort_values("importance", ascending=False)

print("\n=== SHAP Global Feature Importance ===")
print(shap_importance) # we will remove the features like savings_assets_log /
                         #occupation_status_Employed/occupation_status_Self-Employed/occupation_status_Student


######################################################################### WXGB Model (80/10/10 Split)

selected_features = [

    'years_employed_log',
    'current_debt_log',
    'loan_amount_scaled',
    'annual_income_log',
    'credit_history_years_scaled',
    'savings_assets_log',
    'debt_to_income_ratio_scaled',
    'loan_to_income_ratio_scaled',
    'age_scaled',
    'payment_to_income_ratio_scaled',
    'credit_score_scaled',
    'interest_rate_scaled',
    'delinquencies_last_2yrs_binary',
    'derogatory_marks_binary',
    'defaults_on_file',

    'occupation_status_Employed',
    'occupation_status_Self-Employed',
    'occupation_status_Student',

    'product_type_Credit Card',
    'product_type_Line of Credit',
    'product_type_Personal Loan',

    'loan_intent_Business',
    'loan_intent_Debt Consolidation',
    'loan_intent_Education',
    'loan_intent_Home Improvement',
    'loan_intent_Medical',
    'loan_intent_Personal'
]

X = df[selected_features]
y = df["loan_status"]   # must be 0 and 1 only


# =========================
# 80 / 10 / 10 Split
# =========================

from sklearn.model_selection import train_test_split

# Step 1: 80% train, 20% temp
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Step 2: Split 20% into 10% validation and 10% test
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,   # 50% of 20% = 10%
    random_state=42,
    stratify=y_temp
)

print("Train size:", len(X_train))
print("Validation size:", len(X_val))
print("Test size:", len(X_test))


# =========================
# Compute Class Weights
# =========================

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

classes = np.unique(y_train)

weights = compute_class_weight(
    class_weight='balanced',
    classes=classes,
    y=y_train
)

class_weights = dict(zip(classes, weights))
print("Class Weights:", class_weights)

# Create sample weights
sample_weights = y_train.map(class_weights)


# =========================
# Train XGBoost
# =========================

from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=400,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='binary:logistic',
    eval_metric='logloss',
    random_state=42
)

model.fit(
    X_train,
    y_train,
    sample_weight=sample_weights,
    eval_set=[(X_val, y_val)],
    verbose=False
)


# =========================
# Evaluation on TEST set
# =========================

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]


from sklearn.metrics import recall_score

recall_class1 = recall_score(y_test, y_pred, pos_label=1)
recall_class0 = recall_score(y_test, y_pred, pos_label=0)

print("Recall Class 0:", recall_class0)
print("Recall Class 1:", recall_class1)


import numpy as np

gmean = np.sqrt(recall_class0 * recall_class1)
print("G-Mean:", gmean)


from sklearn.metrics import roc_auc_score

auc = roc_auc_score(y_test, y_prob)
print("AUC:", auc)


from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)



