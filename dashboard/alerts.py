import streamlit as st


def show_alerts(df):

    st.subheader("🚨 System Alerts")

    # Get the latest prediction for each node
    latest = (
        df.sort_values("Time")
        .groupby("Node")
        .tail(1)
    )

    # Show nodes whose CURRENT status needs attention
    alerts = latest[
        latest["Status"].isin(
            [
                "Warning",
                "Failure Likely",
                "High Risk"
            ]
        )
    ]

    # No active alerts
    if alerts.empty:

        st.success(
            "✅ No active alerts."
        )

        return

    # Display each active alert
    for _, row in alerts.iterrows():

        st.error(
            f"""
🚨 **{row['Node']}**

Status: **{row['Status']}**

Risk Score: **{row['Risk Score']}%**

Reason: {row['Reasons']}
"""
        )