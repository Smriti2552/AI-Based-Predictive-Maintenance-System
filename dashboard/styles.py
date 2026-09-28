import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        .main {
            background-color: #f5f7fa;
        }

        .metric-card{
            background:white;
            padding:18px;
            border-radius:12px;
            text-align:center;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:10px;
        }

        .node-card{
            background:white;
            border-radius:12px;
            padding:18px;
            margin-bottom:18px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
        }

        .healthy{
            color:#28a745;
            font-weight:bold;
        }

        .warning{
            color:#ff9800;
            font-weight:bold;
        }

        .failure{
            color:#dc3545;
            font-weight:bold;
        }

        </style>
        """,
        unsafe_allow_html=True
    )