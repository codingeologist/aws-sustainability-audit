"""Streamlit Module"""
import streamlit as st
from sustainability.utils import theming
theming()


with st.sidebar:
    st.page_link("streamlit_app.py", label="AWS Sustainability Audit", icon="☁️")
    st.page_link("pages/emissions_report.py", label="AWS Account Emissions Report", icon="🌱")
    st.divider()

st.markdown(
    "<h1 style='text-align: center;'>AWS Sustainability Audit ☁️</h1>",
    unsafe_allow_html=True
)

with open("README.md", "r", encoding="utf-8") as file:
    content = file.read()
st.markdown(content, unsafe_allow_html=True)

# --- Footer ---
with st.bottom:
    st.divider()
    st.markdown(
        '<p style="font-size: 0.8em; color: gray; text-align: right;"> \
            Built with ❤️ by <a href="https://github.com/codingeologist" style="color: gray;"> \
                codingeologist</a></p>',
        unsafe_allow_html=True
    )
