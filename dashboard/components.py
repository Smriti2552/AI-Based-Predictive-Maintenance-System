import streamlit as st


def node_card(node):

    status = node["Status"]

    if status == "Healthy":
        color = "green"
        icon = "🟢"

    elif status == "Warning":
        color = "orange"
        icon = "🟡"

    else:
        color = "red"
        icon = "🔴"

    with st.container(border=True):

        st.subheader(f"{icon} {node['Node']}")

        st.markdown(f"**Status:** :{color}[{status}]")

        st.progress(min(float(node["CPU"]) / 100, 1.0))
        st.caption(f"CPU Usage: {node['CPU']} %")

        st.progress(min(float(node["Memory"]) / 100, 1.0))
        st.caption(f"Memory Usage: {node['Memory']} %")

        st.progress(min(float(node["Network"]) / 100, 1.0))
        st.caption(f"Network Traffic: {node['Network']} %")

        power = float(node["Power"])

        # Assuming max power = 300W for visualization
        st.progress(min(power / 300, 1.0))
        st.caption(f"Power Consumption: {power} W")

        st.markdown("---")

        st.metric(
            "Risk Score",
            f"{node['Risk Score']}%"
        )

        st.info(f"Reason: {node['Reasons']}")