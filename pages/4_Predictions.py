import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Predictions | Predictive Maintenance",
    page_icon="📋",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("📋 Prediction History")
st.caption("Complete AI prediction and telemetry history")

# ============================================================
# LOAD DATA
# ============================================================

REPORT_FILE = "reports/predictions.csv"

if not os.path.exists(REPORT_FILE):
    st.error("Prediction history file not found.")
    st.stop()

df = pd.read_csv(REPORT_FILE)

if df.empty:
    st.warning("No predictions available yet.")
    st.stop()

# Convert time
if "Time" in df.columns:
    df["Time"] = pd.to_datetime(
        df["Time"],
        errors="coerce"
    )

# ============================================================
# SUMMARY METRICS
# ============================================================

total_predictions = len(df)

healthy_predictions = (
    df["Status"].eq("Healthy").sum()
    if "Status" in df.columns
    else 0
)

warning_predictions = (
    df["Status"].eq("Warning").sum()
    if "Status" in df.columns
    else 0
)

high_risk_predictions = (
    df["Status"]
    .isin(["Failure Likely", "High Risk"])
    .sum()
    if "Status" in df.columns
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Predictions",
        total_predictions
    )

with col2:
    st.metric(
        "🟢 Healthy",
        healthy_predictions
    )

with col3:
    st.metric(
        "🟡 Warnings",
        warning_predictions
    )

with col4:
    st.metric(
        "🚨 High Risk",
        high_risk_predictions
    )

# ============================================================
# FILTERS
# ============================================================

st.divider()

st.subheader("🔎 Filter Predictions")

col1, col2 = st.columns(2)

with col1:

    nodes = sorted(
        df["Node"].dropna().unique()
    )

    selected_node = st.selectbox(
        "Select Node",
        ["All Nodes"] + nodes
    )

with col2:

    statuses = sorted(
        df["Status"].dropna().unique()
    )

    selected_status = st.selectbox(
        "Select Status",
        ["All Statuses"] + statuses
    )

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_node != "All Nodes":

    filtered_df = filtered_df[
        filtered_df["Node"] == selected_node
    ]

if selected_status != "All Statuses":

    filtered_df = filtered_df[
        filtered_df["Status"] == selected_status
    ]

# ============================================================
# FILTER RESULT
# ============================================================

st.metric(
    "Predictions Found",
    len(filtered_df)
)

# ============================================================
# PREDICTION TABLE
# ============================================================

st.divider()

st.subheader("📋 Prediction Records")

if filtered_df.empty:

    st.info(
        "No prediction records match the selected filters."
    )

else:

    display_df = (
        filtered_df
        .sort_values(
            "Time",
            ascending=False
        )
        .copy()
    )

    if "Risk Score" in display_df.columns:

        display_df["Risk Score"] = (
            display_df["Risk Score"]
            .round(2)
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# DOWNLOAD
# ============================================================

if not filtered_df.empty:

    st.download_button(
        label="⬇️ Download Filtered Predictions",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_predictions.csv",
        mime="text/csv"
    )