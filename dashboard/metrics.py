import streamlit as st


def show_metrics(df):

    latest = (
        df.sort_values("Time")
          .groupby("Node")
          .tail(1)
    )

    total_nodes = len(latest)

    healthy = (latest["Status"] == "Healthy").sum()

    warning = (latest["Status"] == "Warning").sum()

    failure = (
        (latest["Status"] == "Failure Likely") |
        (latest["Status"] == "High Risk")
    ).sum()

    avg_risk = round(latest["Risk Score"].mean(), 2)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🖥 Total Nodes",
            total_nodes
        )

    with c2:
        st.metric(
            "🟢 Healthy",
            healthy
        )

    with c3:
        st.metric(
            "🟡 Warning",
            warning
        )

    with c4:
        st.metric(
            "📈 Avg Risk",
            f"{avg_risk}%"
        )