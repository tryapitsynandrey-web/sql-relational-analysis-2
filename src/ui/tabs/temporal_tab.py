import streamlit as st
import plotly.express as px

def render_temporal_tab(engine):
    st.header("Temporal Trends & Anomalies")
    
    col1, col2 = st.columns(2)
    
    with st.spinner("Calculating Temporal Metrics..."):
        heatmap_df = engine.fetch_metric('hourly_conversion_heatmap')
        weekend_df = engine.fetch_metric('weekend_degradation')
        anomaly_df = engine.fetch_metric('anomaly_detection')
        
        # High level weekend vs weekday comparison
        if not weekend_df.empty:
            weekday_slice = weekend_df[weekend_df['day_type'] == 'Weekday']['revenue_per_session']
            weekday_rev = weekday_slice.iloc[0] if not weekday_slice.empty else 0
            
            weekend_slice = weekend_df[weekend_df['day_type'] == 'Weekend']['revenue_per_session']
            weekend_rev = weekend_slice.iloc[0] if not weekend_slice.empty else 0
            
            diff = 0
            if weekday_rev > 0:
                diff = ((weekend_rev - weekday_rev) / weekday_rev) * 100
            
            col1.metric("Avg Rev/Session (Weekday)", f"${weekday_rev:,.2f}")
            col2.metric("Avg Rev/Session (Weekend)", f"${weekend_rev:,.2f}", f"{diff:,.2f}%" if diff else None)
        else:
            col1.metric("Avg Rev/Session (Weekday)", "N/A")
            col2.metric("Avg Rev/Session (Weekend)", "N/A")
        
        st.subheader("Hourly Conversion Heatmap (By Day of Week)")
        
        # Plotly Express Density Heatmap
        if not heatmap_df.empty:
            # Map Day of week (0-6) mapping to actual strings
            day_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
            heatmap_df['Day Name'] = heatmap_df['day_of_week'].map(day_map)
            
            fig = px.density_heatmap(
                heatmap_df, 
                x='hour_of_day', 
                y='Day Name', 
                z='conversion_rate', 
                histfunc='avg',
                title="Conversion Rate by Hour and Day (%)",
                labels={'hour_of_day': 'Hour of Day (0-23)', 'conversion_rate': 'Conversion %'},
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Formatted table
            st.dataframe(heatmap_df[['Day Name', 'hour_of_day', 'conversion_rate']].style.format({
                'conversion_rate': '{:.2f}%'
            }), use_container_width=True)
        
        st.subheader("Detected Anomalies (>20% Drop vs 7D Moving Avg)")
        if anomaly_df.empty:
            st.success("No critical statistical anomalies detected in the conversion rates.")
        else:
            st.warning(f"Detected {len(anomaly_df)} days with dangerous conversion drops.")
            st.dataframe(anomaly_df.style.format({
                'daily_cv_rate': '{:.2f}%',
                'moving_7d_avg_cv_rate': '{:.2f}%',
                'drop_percentage': '{:.2f}%'
            }), use_container_width=True)
