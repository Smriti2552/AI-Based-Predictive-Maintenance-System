import os
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Based Predictive Maintenance",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PREDICTIONS_FILE = os.path.join(
    BASE_DIR,
    "reports",
    "predictions.csv"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 35px;
    }

    .status-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30343b;
        background-color: #11151c;
        text-align: center;
    }

    .status-title {
        font-size: 16px;
        color: #b0b6bf;
        margin-bottom: 8px;
    }

    .status-value {
        font-size: 34px;
        font-weight: 700;
    }

    .healthy {
        color: #22c55e;
    }

    .warning {
        color: #facc15;
    }

    .risk {
        color: #60a5fa;
    }

    .alert-box {
        padding: 16px 20px;
        border-radius: 10px;
        background-color: #3a3010;
        border-left: 5px solid #facc15;
        margin-bottom: 10px;
    }

    .healthy-box {
        padding: 18px 20px;
        border-radius: 10px;
        background-color: #123524;
        border-left: 5px solid #22c55e;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD PREDICTIONS
# ============================================================

@st.cache_data(ttl=3)
def load_predictions():

    if not os.path.exists(PREDICTIONS_FILE):
        return pd.DataFrame()

    try:

        df = pd.read_csv(PREDICTIONS_FILE)

        if df.empty:
            return df

        # Convert time column
        if "Time" in df.columns:

            df["Time"] = pd.to_datetime(
                df["Time"],
                errors="coerce"
            )

        # Convert numeric columns
        numeric_columns = [
            "Risk Score",
            "CPU",
            "Memory",
            "Network",
            "Power"
        ]

        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        return df

    except Exception as e:

        st.error(
            f"Unable to read prediction data: {e}"
        )

        return pd.DataFrame()


df = load_predictions()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI-Based Predictive Maintenance Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    Real-time overview of infrastructure health and
    predictive maintenance risk
    """,
    unsafe_allow_html=True
)


# ============================================================
# NO DATA
# ============================================================

if df.empty:

    st.warning(
        "No predictions available. "
        "Start the MQTT consumer and monitoring nodes "
        "to generate predictions."
    )

    st.stop()


# ============================================================
# GET LATEST PREDICTION FOR EACH NODE
# ============================================================

if "Time" in df.columns:

    df = df.sort_values(
        "Time"
    )


latest = (
    df
    .groupby("Node", as_index=False)
    .tail(1)
    .copy()
)


# ============================================================
# SUMMARY METRICS
# ============================================================

total_nodes = latest["Node"].nunique()


healthy_count = (
    latest["Status"]
    .eq("Healthy")
    .sum()
)


warning_count = (
    latest["Status"]
    .eq("Warning")
    .sum()
)


failure_count = (
    latest["Status"]
    .isin(
        [
            "Failure Likely",
            "High Risk"
        ]
    )
    .sum()
)


avg_risk = (
    latest["Risk Score"]
    .mean()
)


# ============================================================
# TOP SUMMARY CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">🖥️ Total Nodes</div>
            <div class="status-value">%d</div>
        </div>
        """
        % total_nodes,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">🟢 Healthy</div>
            <div class="status-value healthy">%d</div>
        </div>
        """
        % healthy_count,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">🟡 Warning</div>
            <div class="status-value warning">%d</div>
        </div>
        """
        % warning_count,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">📈 Average Risk</div>
            <div class="status-value risk">%.2f%%</div>
        </div>
        """
        % avg_risk,
        unsafe_allow_html=True
    )


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.divider()

st.subheader("📊 System Overview")


overview_col1, overview_col2 = st.columns(2)


with overview_col1:

    if failure_count > 0:

        st.error(
            f"🚨 {failure_count} node(s) have a high failure risk."
        )

    elif warning_count > 0:

        st.warning(
            f"⚠️ {warning_count} node(s) currently require attention."
        )

    else:

        st.success(
            "✅ All monitored nodes are currently healthy."
        )


with overview_col2:

    if "Risk Score" in latest.columns:

        highest_risk_row = latest.loc[
            latest["Risk Score"].idxmax()
        ]

        highest_node = highest_risk_row["Node"]

        highest_risk = highest_risk_row["Risk Score"]

        st.info(
            f"📌 Highest current risk: **{highest_node}** "
            f"with **{highest_risk:.2f}%** risk."
        )


# ============================================================
# CURRENT ALERTS
# ============================================================

st.divider()

st.subheader("🚨 Current Alerts")


problem_nodes = latest[
    latest["Status"].isin(
        [
            "Warning",
            "Failure Likely",
            "High Risk"
        ]
    )
].copy()


if problem_nodes.empty:

    st.markdown(
        """
        <div class="healthy-box">
            ✅ No active alerts. All nodes are operating normally.
        </div>
        """,
        unsafe_allow_html=True
    )


else:

    for _, row in problem_nodes.iterrows():

        node = row["Node"]

        status = row["Status"]

        risk = row["Risk Score"]

        reasons = row.get(
            "Reasons",
            "Abnormal condition detected"
        )

        st.markdown(
            f"""
            <div class="alert-box">
                <strong>⚠️ {node} — {status}</strong><br>
                Risk Score: <strong>{risk:.2f}%</strong><br>
                Reason: {reasons}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# LAST UPDATE
# ============================================================

st.divider()


if "Time" in latest.columns:

    latest_time = latest["Time"].max()

    if pd.notna(latest_time):

        st.caption(
            f"Last prediction received: {latest_time}"
        )


st.caption(
    "Use the navigation menu on the left to explore "
    "Nodes, Alerts, Analytics and Predictions."
)