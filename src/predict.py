import os
import joblib
import pandas as pd
from datetime import datetime


# ==========================
# Load Models
# ==========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


rf_model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "random_forest.pkl"
    )
)


xgb_model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "xgboost.pkl"
    )
)


scaler = joblib.load(
    os.path.join(
        MODEL_DIR,
        "scaler.pkl"
    )
)


# ==========================
# Prediction Function
# ==========================

def predict(data):

    # ==========================
    # LabelEncoder Mappings
    # ==========================

    # LabelEncoder sorts values
    # alphabetically.

    task_type_map = {
        "CPU": 0,
        "IO": 1,
        "Memory": 2,
        "Network": 3
    }


    task_priority_map = {
        "High": 0,
        "Low": 1,
        "Medium": 2
    }


    task_status_map = {
        "Completed": 0,
        "Failed": 1,
        "Running": 2
    }


    # ==========================
    # Current Date/Time
    # ==========================

    now = datetime.now()

    hour = now.hour
    day = now.day
    month = now.month


    # ==========================
    # Prepare Features
    # ==========================

    features = pd.DataFrame(
        [[
            data["cpu_usage"],
            data["memory_usage"],
            data["network_traffic"],
            data["power_consumption"],
            data["num_executed_instructions"],
            data["execution_time"],
            data["energy_efficiency"],

            task_type_map.get(
                data["task_type"],
                0
            ),

            task_priority_map.get(
                data["task_priority"],
                0
            ),

            task_status_map.get(
                data["task_status"],
                0
            ),

            hour,
            day,
            month
        ]],
        columns=[
            "cpu_usage",
            "memory_usage",
            "network_traffic",
            "power_consumption",
            "num_executed_instructions",
            "execution_time",
            "energy_efficiency",
            "task_type",
            "task_priority",
            "task_status",
            "hour",
            "day",
            "month"
        ]
    )


    # ==========================
    # Make Sure Feature Order
    # Matches Training
    # ==========================

    if hasattr(
        scaler,
        "feature_names_in_"
    ):

        features = features[
            scaler.feature_names_in_
        ]


    # ==========================
    # Scale Features
    # ==========================

    scaled_features = scaler.transform(
        features
    )


    # ==========================
    # Random Forest Prediction
    # ==========================

    rf_probability = (
        rf_model.predict_proba(
            scaled_features
        )[0][1]
    )


    # ==========================
    # XGBoost Prediction
    # ==========================

    xgb_probability = (
        xgb_model.predict_proba(
            scaled_features
        )[0][1]
    )


    # ==========================
    # Average Both Models
    # ==========================

    risk_score = (
        (
            rf_probability +
            xgb_probability
        ) / 2
    ) * 100


    risk_score = round(
        risk_score,
        2
    )


    # ==========================
    # Failure Explanation
    # ==========================

    reasons = []


    if data["cpu_usage"] > 85:

        reasons.append(
            "High CPU Usage"
        )


    if data["memory_usage"] > 85:

        reasons.append(
            "High Memory Usage"
        )


    if data["power_consumption"] > 300:

        reasons.append(
            "High Power Consumption"
        )


    if data["network_traffic"] > 80:

        reasons.append(
            "High Network Traffic"
        )


    # ==========================
    # Status Decision
    # ==========================

    if risk_score >= 70:

        status = "Failure Likely"

    elif len(reasons) >= 1:

        status = "Warning"

    else:

        status = "Healthy"


    # ==========================
    # Default Reason
    # ==========================

    if len(reasons) == 0:

        reasons.append(
            "No abnormal conditions detected"
        )


    # ==========================
    # Return Prediction
    # ==========================

    return {

        "status": status,

        "risk_score": risk_score,

        "reasons": reasons

    }