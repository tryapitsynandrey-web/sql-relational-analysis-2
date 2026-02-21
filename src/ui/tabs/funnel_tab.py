import streamlit as st
import plotly.express as px
import pandas as pd

def render_funnel_tab(engine):
    st.header("Funnels & Conversion")
    
    col1, col2, col3 = st.columns(3)
    
    with st.spinner("Calculating Funnel Metrics..."):
        funnel_df = engine.fetch_metric('view_to_cart_funnel')
        cart_abandon_df = engine.fetch_metric('cart_abandonment_rate')
        ttf_df = engine.fetch_metric('time_to_first_purchase')
        
        v2c = funnel_df.iloc[0]['view_to_cart_rate'] if not funnel_df.empty else 0
        c2p = funnel_df.iloc[0]['cart_to_purchase_rate'] if not funnel_df.empty else 0
        latest_abandon = cart_abandon_df.iloc[0]['cart_abandonment_rate'] if not cart_abandon_df.empty else 0
        
        col1.metric("View-to-Cart", f"{v2c}%")
        col2.metric("Cart-to-Purchase", f"{c2p}%")
        col3.metric("Latest Cart Abandonment", f"{latest_abandon}%")
        
        st.subheader("Daily Cart Abandonment Rate")
        if not cart_abandon_df.empty:
            fig_abandon = px.line(
                cart_abandon_df, 
                x='act_date', 
                y='cart_abandonment_rate',
                title="Cart Abandonment Trend (%)",
                labels={'act_date': 'Date', 'cart_abandonment_rate': 'Abandonment Rate (%)'}
            )
            fig_abandon.update_traces(line=dict(width=3, color='#e74c3c'))
            st.plotly_chart(fig_abandon, use_container_width=True)
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Overall Funnel Drop-off")
            if not funnel_df.empty:
                funnel_data = pd.DataFrame(dict(
                    val=[funnel_df.iloc[0]['viewed_product'], funnel_df.iloc[0]['added_to_cart'], funnel_df.iloc[0]['purchased']],
                    stage=["Viewed", "Carted", "Purchased"]
                ))
                fig_funnel = px.funnel(funnel_data, x='val', y='stage', title="Macro View-to-Purchase Funnel")
                st.plotly_chart(fig_funnel, use_container_width=True)
            
        with col_chart2:
            st.subheader("Time to First Purchase Distribution")
            if not ttf_df.empty:
                fig_ttf = px.bar(
                    ttf_df,
                    x='time_segment',
                    y='pct_of_purchasers',
                    color='time_segment',
                    title="% of Purchasers by Time to Convert",
                    labels={'time_segment': 'Time Segment', 'pct_of_purchasers': '% of Purchasers'},
                    color_discrete_sequence=px.colors.sequential.Teal
                )
                fig_ttf.update_layout(showlegend=False)
                st.plotly_chart(fig_ttf, use_container_width=True)
