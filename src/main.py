import os
import sys
import streamlit as st

st.set_page_config(page_title="SQL Relational Analysis v2", layout="wide")

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.dashboard import render_dashboard

if __name__ == "__main__":
    render_dashboard()