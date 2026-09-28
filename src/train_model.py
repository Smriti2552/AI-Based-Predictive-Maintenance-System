import os
import joblib

from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
from xgboost import XGBClassifier

# ==========================
# Load Processed Data
# ==========================

X_train, X_test, y_train, y_test = joblib.load(
    "models/processed_data.pkl"
)

print("Original Training Distribution:")
print(y_train.value_counts())

# ==========================
# Apply SMOTE
# ==========================

smote = SMOTE(random_state=42)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train,
    y_train
)

print("\nBalanced Training Distribution:")
print(y_train_balanced.value_counts())

# ==========================
# Random Forest
# ==========================

print("\nTraining Random Forest...\n")

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

rf.fit(X_train_balanced, y_train_balanced)

rf_pred = rf.predict(X_test)

print("=" * 50)
print("Random Forest Results")
print("=" * 50)

print("Accuracy:", accuracy_score(y_test, rf_pred))
print()

print(classification_report(y_test, rf_pred))

print("Confusion Matrix")
print(confusion_matrix(y_test, rf_pred))

# ==========================
# XGBoost
# ==========================

print("\nTraining XGBoost...\n")

xgb = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)

xgb.fit(X_train_balanced, y_train_balanced)

xgb_pred = xgb.predict(X_test)

print("\n" + "=" * 50)
print("XGBoost Results")
print("=" * 50)

print("Accuracy:", accuracy_score(y_test, xgb_pred))
print()

print(classification_report(y_test, xgb_pred))

print("Confusion Matrix")
print(confusion_matrix(y_test, xgb_pred))

# ==========================
# Save Models
# ==========================

os.makedirs("models", exist_ok=True)

joblib.dump(rf, "models/random_forest.pkl")
joblib.dump(xgb, "models/xgboost.pkl")

print("\nModels saved successfully!")