import streamlit as st
import pandas as pd
import os

from dashboard.components import node_card


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nodes | Predictive Maintenance",
    page_icon="🖥️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🖥️ Machine Nodes")

st.caption(
    "Real-time condition monitoring of factory machines"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

REPORT_FILE = os.path.join(
    BASE_DIR,
    "reports",
    "predictions.csv"
)


# ============================================================
# CHECK PREDICTION FILE
# ============================================================

if not os.path.exists(REPORT_FILE):

    st.error(
        "Prediction history file not found."
    )

    st.stop()


# ============================================================
# LOAD PREDICTIONS
# ============================================================

df = pd.read_csv(
    REPORT_FILE
)


if df.empty:

    st.warning(
        "No predictions available yet."
    )

    st.stop()


# ============================================================
# CONVERT TIME
# ============================================================

df["Time"] = pd.to_datetime(
    df["Time"],
    errors="coerce"
)


# ============================================================
# LATEST PREDICTION PER NODE
# ============================================================

latest_nodes = (
    df
    .sort_values("Time")
    .groupby("Node")
    .tail(1)
)


# ============================================================
# CURRENT NODE STATUS
# ============================================================

st.subheader(
    "Current Node Status"
)


nodes = latest_nodes.to_dict(
    "records"
)


# ============================================================
# DISPLAY NODE CARDS
# ============================================================

columns = st.columns(2)


for i, node in enumerate(nodes):

    with columns[i % 2]:

        node_card(node)