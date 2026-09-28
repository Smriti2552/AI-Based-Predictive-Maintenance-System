import streamlit as st
import pandas as pd
import os

from dashboard.alerts import show_alerts


st.set_page_config(
    page_title="Alerts | Predictive Maintenance",
    page_icon="🚨",
    layout="wide"
)


st.title("🚨 Maintenance Alerts")
st.caption("Active warnings and predicted machine failures")


REPORT_FILE = "reports/predictions.csv"


if not os.path.exists(REPORT_FILE):

    st.error("Prediction history file not found.")

    st.stop()


df = pd.read_csv(REPORT_FILE)


if df.empty:

    st.warning("No predictions available yet.")

    st.stop()


df["Time"] = pd.to_datetime(
    df["Time"]
)


# ==========================
# Current alerts
# ==========================

show_alerts(df)


# ==========================
# Recent warning history
# ==========================

st.divider()

st.subheader("Recent Warning History")


warnings = df[
    df["Status"].isin(
        ["Warning", "Failure Likely"]
    )
].sort_values(
    "Time",
    ascending=False
)


if warnings.empty:

    st.success(
        "No warning or failure events recorded."
    )

else:

    st.dataframe(
        warnings,
        use_container_width=True,
        hide_index=True
    )