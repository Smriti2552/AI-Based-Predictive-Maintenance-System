import streamlit as st


def risk_chart(df):

    st.subheader("📈 Risk Score Trend")

    chart = df.pivot_table(
        index="Time",
        columns="Node",
        values="Risk Score",
        aggfunc="last"
    )

    st.line_chart(chart)

    st.subheader("⚡ Current CPU Usage")

    latest = (
        df.sort_values("Time")
          .groupby("Node")
          .tail(1)
          .set_index("Node")
    )

    st.bar_chart(latest["CPU"])


def prediction_table(df):

    st.subheader("📋 Prediction History")

    st.dataframe(
        df.sort_values("Time", ascending=False),
        use_container_width=True
    )