import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Analytics | Predictive Maintenance",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📈 System Analytics")
st.caption("Historical machine performance and risk trends")


# ============================================================
# LOAD PREDICTIONS
# ============================================================

REPORT_FILE = "reports/predictions.csv"

if not os.path.exists(REPORT_FILE):

    st.error(
        "Prediction history file not found."
    )

    st.stop()


df = pd.read_csv(REPORT_FILE)


if df.empty:

    st.warning(
        "No predictions available yet."
    )

    st.stop()


# ============================================================
# PREPARE DATA
# ============================================================

df["Time"] = pd.to_datetime(
    df["Time"],
    errors="coerce"
)

df["Risk Score"] = pd.to_numeric(
    df["Risk Score"],
    errors="coerce"
)

df["CPU"] = pd.to_numeric(
    df["CPU"],
    errors="coerce"
)

df["Memory"] = pd.to_numeric(
    df["Memory"],
    errors="coerce"
)

df["Network"] = pd.to_numeric(
    df["Network"],
    errors="coerce"
)

df["Power"] = pd.to_numeric(
    df["Power"],
    errors="coerce"
)


# ============================================================
# ANALYTICS SUMMARY
# ============================================================

total_records = len(df)

average_risk = df["Risk Score"].mean()

highest_risk_row = df.loc[
    df["Risk Score"].idxmax()
]

highest_risk_node = highest_risk_row["Node"]

highest_risk = highest_risk_row["Risk Score"]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📊 Total Predictions",
        total_records
    )


with col2:

    st.metric(
        "📈 Average Risk",
        f"{average_risk:.2f}%"
    )


with col3:

    st.metric(
        "🚨 Highest Risk",
        f"{highest_risk_node} — {highest_risk:.2f}%"
    )


st.divider()


# ============================================================
# NODE FILTER
# ============================================================

nodes = sorted(
    df["Node"].dropna().unique()
)

selected_node = st.selectbox(
    "Select Node",
    ["All Nodes"] + nodes
)


if selected_node != "All Nodes":

    chart_df = df[
        df["Node"] == selected_node
    ].copy()

else:

    chart_df = df.copy()


# ============================================================
# RISK SCORE
# ============================================================

st.subheader("⚠️ Risk Score History")

st.line_chart(
    chart_df.set_index("Time")[
        "Risk Score"
    ]
)


# ============================================================
# CPU
# ============================================================

st.subheader("🖥️ CPU Usage")

st.line_chart(
    chart_df.set_index("Time")[
        "CPU"
    ]
)


# ============================================================
# MEMORY
# ============================================================

st.subheader("💾 Memory Usage")

st.line_chart(
    chart_df.set_index("Time")[
        "Memory"
    ]
)


# ============================================================
# NETWORK
# ============================================================

st.subheader("🌐 Network Traffic")

st.line_chart(
    chart_df.set_index("Time")[
        "Network"
    ]
)


# ============================================================
# POWER
# ============================================================

st.subheader("⚡ Power Consumption")

st.line_chart(
    chart_df.set_index("Time")[
        "Power"
    ]
)


# ============================================================
# LAST UPDATE
# ============================================================

latest_time = df["Time"].max()

if pd.notna(latest_time):

    st.divider()

    st.caption(
        f"Latest prediction received: {latest_time}"
    )