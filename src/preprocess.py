import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("dataset/Cloud_Anomaly_Dataset.csv")

print("Original Shape:", df.shape)

# ==========================
# Remove unnecessary column
# ==========================

df.drop(columns=["vm_id"], inplace=True)

# ==========================
# Timestamp
# ==========================

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.month

df.drop(columns=["timestamp"], inplace=True)

# ==========================
# Fill Missing Values
# ==========================

# Numerical columns
num_cols = [
    "cpu_usage",
    "memory_usage",
    "network_traffic",
    "power_consumption",
    "num_executed_instructions",
    "execution_time",
    "energy_efficiency",
]

for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Categorical columns
cat_cols = [
    "task_type",
    "task_priority",
    "task_status",
]

for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# ==========================
# Encode Categories
# ==========================

encoder = LabelEncoder()

for col in cat_cols:
    df[col] = encoder.fit_transform(df[col])

# ==========================
# Final Safety Check
# ==========================

print("\nMissing values before split:")
print(df.isnull().sum())

# If ANY NaN still exists, replace it
df = df.fillna(0)

# ==========================
# Features & Target
# ==========================

X = df.drop(columns=["Anomaly status"])
y = df["Anomaly status"]

# ==========================
# Train/Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================
# Scaling
# ==========================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ==========================
# Verify
# ==========================

print("\nNaN after scaling:")
print(np.isnan(X_train).sum())
print(np.isnan(X_test).sum())

# ==========================
# Save
# ==========================

joblib.dump(
    (X_train, X_test, y_train, y_test),
    "models/processed_data.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

print("\nPreprocessing Completed Successfully!")