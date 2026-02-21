import streamlit as st
import plotly.express as px

def render_behavior_tab(engine):
    st.header("User Behavior & Retention")
    
    col1, col2, col3 = st.columns(3)
    
    with st.spinner("Calculating Behavior Metrics..."):
        retention_df = engine.fetch_metric('cohort_retention')
        dau_mau_df = engine.fetch_metric('dau_mau_ratio')
        rfm_df = engine.fetch_metric('rfm_segments')
        basket_df = engine.fetch_metric('market_basket_pairs')
        
        latest_dau_mau = dau_mau_df.iloc[0]['dau_mau_ratio_pct'] if not dau_mau_df.empty else 0
        latest_30d_ret = retention_df.iloc[0]['retention_rate_30d'] if not retention_df.empty else 0
        champions_slice = rfm_df[rfm_df['rfm_segment'] == 'Champions']['customer_count']
        total_champions = champions_slice.iloc[0] if not champions_slice.empty else 0
        
        col1.metric("DAU/MAU Stickiness", f"{latest_dau_mau}%")
        col2.metric("Latest 30d Retention", f"{latest_30d_ret}%")
        col3.metric("Champion Customers", f"{total_champions:,}")
        
        st.subheader("DAU/MAU Ratio Trend")
        if not dau_mau_df.empty:
            fig_dau = px.line(
                dau_mau_df, 
                x='act_date', 
                y='dau_mau_ratio_pct',
                title="DAU / MAU Stickiness (%)",
                labels={'act_date': 'Date', 'dau_mau_ratio_pct': 'Ratio (%)'}
            )
            fig_dau.update_traces(line=dict(width=3, color='#8e44ad'))
            st.plotly_chart(fig_dau, use_container_width=True)
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("RFM Segments Distribution")
            if not rfm_df.empty:
                fig_rfm = px.bar(
                    rfm_df,
                    x='rfm_segment',
                    y='customer_count',
                    color='rfm_segment',
                    title="Customer Valuation Quadrants",
                    labels={'rfm_segment': 'Segment', 'customer_count': 'Customer Count'},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_rfm.update_layout(showlegend=False)
                st.plotly_chart(fig_rfm, use_container_width=True)
            
        with col_chart2:
            st.subheader("Top Market Basket Pairs")
            formatted_basket = basket_df.head(10).rename(columns={'product_a': 'Product A', 'product_b': 'Product B', 'co_purchase_count': 'Co-Purchases'})
            st.dataframe(formatted_basket[['Product A', 'Product B', 'Co-Purchases']], use_container_width=True)
