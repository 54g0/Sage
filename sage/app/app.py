# app.py

import streamlit as st
import pandas as pd
import os
import sys
from typing import Dict, List
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sage.utils.get_insight import get_insights
from sage.utils.get_analysis import get_analysis_from_D2C
from dotenv import load_dotenv

load_dotenv()

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize session state
if "app_insights" not in st.session_state:
    st.session_state.app_insights = None
if "d2c_analysis" not in st.session_state:
    st.session_state.d2c_analysis = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
# Custom CSS for better design
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.stButton>button {
    background-color: #4a90e2;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}
.stSidebar .sidebar-content {
    background-color: #e6f3ff;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for D2C button
with st.sidebar:
    st.header("📦 D2C eCommerce")
    if st.button("🔍 Run D2C Analysis"):
        with st.spinner("Analyzing D2C data..."):
            try:
                st.session_state.d2c_analysis = get_analysis_from_D2C()
            except Exception as e:
                st.error(f"Error: {e}")

# Main content
st.set_page_config(page_title="Sage- Market Intelligence", layout="wide")

st.title("Sage- Market Intelligence Dashboard")
st.markdown("Analyze app store trends and D2C performance with AI-powered insights.")

# Input fields
categories = [
    'AUTO_AND_VEHICLES', 'BEAUTY', 'BOOKS_AND_REFERENCE',
    'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING',
    'EDUCATION', 'ENTERTAINMENT', 'EVENTS', 'FINANCE', 'FOOD_AND_DRINK'
]

col1, col2, col3 = st.columns(3)

with col1:
    selected_category = st.selectbox("Google Play Store Category", categories)

with col2:
    custom_query = st.text_input("🔍 App Store (e.g., 'top-apps')", "")

with col3:
    custom_query_1 = st.text_input("App Store Genre (e.g., 'gaming')", "")

# Generate App Insights
if st.button("Generate App Insights"):
    with st.spinner("Analyzing Google Play Store data..."):
        try:
            
            insights, llm_response ,report= get_insights(selected_category, custom_query, custom_query_1)
            st.session_state.app_insights = llm_response
            st.session_state.report_generated = report
            st.session_state.selected_category = selected_category
        except Exception as e:
            st.error(f"Error: {e}")

# Display App Insights
if st.session_state.app_insights:
    st.subheader(" App Store Insights")
    st.markdown(f"<div style='background-color:black; padding:15px; border-radius:8px; border-left:4px solid #4a90e2;'>{st.session_state.app_insights}</div>", unsafe_allow_html=True)
if st.session_state.report_generated:
    st.subheader("Comprehensive Report")
    st.markdown(f"<div style='background-color:black; padding:15px; border-radius:8px; border-left:4px solid #e74c3c;'>{st.session_state.report_generated}</div>", unsafe_allow_html=True)

if st.session_state.d2c_analysis:
    st.subheader("D2C eCommerce Analysis")
    st.markdown(f"<div style='background-color:black; padding:15px; border-radius:8px; border-left:4px solid #e74c3c;'>{st.session_state.d2c_analysis}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Built using Streamlit")