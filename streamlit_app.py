"""Streamlit Module"""
import streamlit as st
from sustainability.utils import theming
theming()


st.set_page_config(
    page_title="AWS Sustainability Audit",
    page_icon="🌱",
)

with st.sidebar:
    st.page_link("streamlit_app.py", label="AWS Sustainability Audit", icon="🌱")
    st.page_link("pages/emissions_report.py", label="AWS Account Emissions Report", icon="☁️")
    st.divider()

st.markdown(
    "<h1 style='text-align: center;'>AWS Sustainability Audit ☁️</h1>",
    unsafe_allow_html=True
)

try:
    with open("AUDIT.md", "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    try:
        with open("README.md", "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        content = "# FIle not found: AUDIT.md or README.md"
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
