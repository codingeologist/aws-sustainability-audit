"""utility helper module"""
import json
from datetime import datetime
import streamlit as st
from sustainability.database import Database


class DateTimeEncoder(json.JSONEncoder):
    """datetime encoder for json exports"""
    def default(self, obj):
        """datetime obj to str"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def export_data(db_path: str, table_name: str, filename: str) -> None:
    """
    export data to file
    """

    db = Database(db_path=db_path)
    df = db.read_table(name=table_name)
    df.to_csv(filename, index=False)


def theming():
    """
    Streamlit theming
    """

    # Hide Streamlit's default header/footer
    hide_st_style = """
        <style>
        /* Hide Deploy button */
        [data-testid="stAppDeployButton"] {
            display: none !important;
        }
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True