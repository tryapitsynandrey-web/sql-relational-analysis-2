import streamlit as st

def render_dependencies_tab(engine):
    st.header("Metric Dependencies & Correlations")
    st.markdown("""
    This section visualizes the cross-metric dependencies showing exactly how behavioral changes alter economic realities within the system.
    """)
    
    with st.spinner("Correlating Metrics..."):
        time_aov_df = engine.fetch_metric('time_of_day_aov_correlation')
        
        st.subheader("How Time-of-Day Affects Average Order Value")
        st.markdown("*Insight: Customers shopping late at night may yield differently sized baskets than midday shoppers.*")
        
        # Dual axis representation using columns since streamlit doesn't natively support dual axis without Plotly/Altair
        col1, col2 = st.columns(2)
        
        chart_df = time_aov_df.rename(columns={'hour_of_day': 'Hour of Day', 'total_orders': 'Total Orders', 'aov': 'AOV'}).set_index('Hour of Day')
        
        with col1:
            st.markdown("**Total Orders by Hour**")
            st.bar_chart(chart_df['Total Orders'])
            
        with col2:
            st.markdown("**Average Order Value by Hour**")
            st.line_chart(chart_df['AOV'])
            
        st.subheader("Raw Data Matrix")
        formatted_df = time_aov_df.rename(columns={'hour_of_day': 'Hour of Day', 'total_orders': 'Total Orders', 'total_revenue': 'Total Revenue', 'aov': 'AOV', 'aov_rank': 'AOV Rank'})
        st.dataframe(formatted_df.style.format({
            'Total Revenue': '${:,.2f}',
            'AOV': '${:,.2f}'
        }), use_container_width=True)
