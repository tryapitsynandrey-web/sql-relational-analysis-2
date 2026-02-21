import streamlit as st
import plotly.express as px

def render_revenue_tab(engine):
    st.header("Revenue & Economics")
    
    with st.spinner("Calculating Revenue Metrics..."):
        aov_df = engine.fetch_metric('aov_trends')
        ltv_df = engine.fetch_metric('ltv_by_cohort')
        deg_df = engine.fetch_metric('revenue_degradation')
        
        # Calculate dynamic KPIs with exact deltas
        latest_aov = aov_df.iloc[0]['aov'] if not aov_df.empty else 0
        prev_aov = aov_df.iloc[1]['aov'] if len(aov_df) > 1 else 0
        aov_delta = latest_aov - prev_aov
        
        latest_rev = deg_df.iloc[0]['daily_revenue'] if not deg_df.empty else 0
        prev_rev = deg_df.iloc[1]['daily_revenue'] if len(deg_df) > 1 else 0
        rev_delta = latest_rev - prev_rev
        
        latest_wow = deg_df.iloc[0]['wow_growth_pct'] if not deg_df.empty else 0
        
        total_cohorts = len(ltv_df['cohort_month'].unique()) if not ltv_df.empty else 0
        
        # Render Top KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest AOV", f"${latest_aov:,.2f}", f"${aov_delta:,.2f}")
        col2.metric("Latest Daily Rev", f"${latest_rev:,.2f}", f"${rev_delta:,.2f} ({latest_wow:.1f}% WoW)")
        col3.metric("Monitored Cohorts", total_cohorts)
        
        # Dynamic Insight Banner
        if not aov_df.empty and not ltv_df.empty:
            direction = "positive" if latest_wow > 0 else "negative"
            best_cohort_idx = ltv_df.groupby('cohort_month')['cumulative_ltv'].max().idxmax()
            best_cohort_val = ltv_df.groupby('cohort_month')['cumulative_ltv'].max().max()
            
            # Format datetime cohort index securely
            if hasattr(best_cohort_idx, 'strftime'):
                best_cohort_str = best_cohort_idx.strftime('%b %Y')
            else:
                best_cohort_str = str(best_cohort_idx)[:7]

            st.info(f"💡 **Revenue Insight:** The strongest cohort is **{best_cohort_str}** hitting an LTV of **${best_cohort_val:,.2f}**. " 
                    f"Overall revenue is carrying a {direction} WoW growth trajectory of {latest_wow:.1f}%.")

        st.divider()

        # CHART 1: AOV Trends
        st.subheader("AOV vs 7-Day Moving Average")
        if not aov_df.empty:
            aov_df_melted = aov_df.melt(id_vars=['act_date'], value_vars=['aov', 'moving_7d_aov'], 
                                        var_name='Metric', value_name='Value')
            aov_df_melted['Metric'] = aov_df_melted['Metric'].map({'aov': 'Daily AOV', 'moving_7d_aov': '7-Day Average'})
            
            fig_aov = px.line(
                aov_df_melted, 
                x="act_date", 
                y="Value", 
                color="Metric",
                title="Average Order Value Trends",
                labels={"act_date": "Date", "Value": "Amount ($)"}
            )
            # Make the Daily AOV slightly transparent
            fig_aov.update_traces(opacity=0.4, selector=dict(name="Daily AOV"))
            fig_aov.update_traces(line=dict(width=3), selector=dict(name="7-Day Average"))
            fig_aov.update_yaxes(tickprefix="$")
            st.plotly_chart(fig_aov, use_container_width=True)
        
        col_chart1, col_chart2 = st.columns(2)
        
        # CHART 2: Revenue Degradation
        with col_chart1:
            st.subheader("Revenue Degradation (WoW)")
            if not deg_df.empty:
                # Filter out first 3 days (outliers from data seeding)
                filtered_deg = deg_df.iloc[3:].copy()
                # Conditional coloring
                filtered_deg['Color'] = filtered_deg['wow_growth_pct'].apply(lambda x: 'Positive' if x >= 0 else 'Negative')
                
                fig_deg = px.bar(
                    filtered_deg, 
                    x='report_date', 
                    y='wow_growth_pct',
                    color='Color',
                    color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c'},
                    title="Week-over-Week Growth",
                    labels={'report_date': 'Date', 'wow_growth_pct': 'WoW Growth (%)'}
                )
                fig_deg.update_layout(showlegend=False)
                st.plotly_chart(fig_deg, use_container_width=True)
            
        # CHART 3: LTV
        with col_chart2:
            st.subheader("Cohort LTV Growth")
            if not ltv_df.empty:
                # Clean up cohort month to string
                ltv_df['Cohort Month'] = ltv_df['cohort_month'].dt.strftime('%b %Y')
                
                fig_ltv = px.line(
                    ltv_df, 
                    x="months_since_first_purchase", 
                    y="cumulative_ltv", 
                    color="Cohort Month",
                    title="Cumulative LTV by Monthly Cohort",
                    labels={
                        "months_since_first_purchase": "Months Since First Purchase",
                        "cumulative_ltv": "Cumulative LTV ($)"
                    },
                    markers=True
                )
                fig_ltv.update_traces(
                    hovertemplate="<b>%{data.name}</b><br>Month %{x}: $%{y:,.2f}<extra></extra>"
                )
                # Force X-axis to integers
                fig_ltv.update_xaxes(dtick=1)
                fig_ltv.update_yaxes(tickprefix="$")
                
                st.plotly_chart(fig_ltv, use_container_width=True)
