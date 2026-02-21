import streamlit as st
from src.core.metric_engine import MetricEngine
from src.db.db_client import DBClient

# Import UI Components
from src.ui.tabs.revenue_tab import render_revenue_tab
from src.ui.tabs.behavior_tab import render_behavior_tab
from src.ui.tabs.funnel_tab import render_funnel_tab
from src.ui.tabs.temporal_tab import render_temporal_tab
from src.ui.tabs.dependencies_tab import render_dependencies_tab
from src.ui.tabs.executive_summary import render_executive_summary

def render_dashboard():
    # st.set_page_config must be called in main.py, so we assume it has been.
    st.title("E-Commerce Behavioral Analytics")
    
    st.sidebar.header("Platform Data")
    st.sidebar.info("SQL-First logic pipeline processing 30+ interconnected metrics.")
    
    db_client = DBClient()
    engine = MetricEngine(db_client)
    
    st.sidebar.metric("Active Models", len(engine.metrics_config))
    
    tab_exec, tab_rev, tab_beh, tab_fun, tab_temp, tab_dep = st.tabs([
        "Executive Summary", 
        "Revenue & Economics", 
        "User Behavior & Retention", 
        "Funnels & Conversion", 
        "Temporal Trends", 
        "Metric Dependencies"
    ])
    
    with tab_exec:
        render_executive_summary(engine)
        
    with tab_rev:
        render_revenue_tab(engine)
        
    with tab_beh:
        render_behavior_tab(engine)
        
    with tab_fun:
        render_funnel_tab(engine)
        
    with tab_temp:
        render_temporal_tab(engine)
        
    with tab_dep:
        render_dependencies_tab(engine)
            
if __name__ == "__main__":
    render_dashboard()
