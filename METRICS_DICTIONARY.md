# Metrics Dictionary

This document is auto-generated from `config/metrics.yaml`.

## Aov Trends
- **Domain**: revenue
- **Description**: Average Order Value (AOV) smoothed with a 7-day moving average.
- **SQL File**: `src/models/marts/aov_trends.sql`

## Ltv By Cohort
- **Domain**: revenue
- **Description**: Customer Lifetime Value tracking cumulative revenue by acquisition cohort.
- **SQL File**: `src/models/marts/ltv_by_cohort.sql`

## Revenue Degradation
- **Domain**: revenue
- **Description**: Month-over-month and week-over-week revenue degradation analysis.
- **SQL File**: `src/models/marts/revenue_degradation.sql`

## Cohort Retention
- **Domain**: behavior
- **Description**: User cohort retention rates over 7, 14, and 30 days.
- **SQL File**: `src/models/marts/cohort_retention.sql`

## Dau Mau Ratio
- **Domain**: behavior
- **Description**: Daily Active Users to Monthly Active Users stickiness ratio.
- **SQL File**: `src/models/marts/dau_mau_ratio.sql`

## Rfm Segments
- **Domain**: behavior
- **Description**: Customer segmentation by Recency, Frequency, and Monetary value clusters.
- **SQL File**: `src/models/marts/rfm_segments.sql`

## Market Basket Pairs
- **Domain**: behavior
- **Description**: Frequent itemsets purchased together in the same cart.
- **SQL File**: `src/models/marts/market_basket_pairs.sql`

## View To Cart Funnel
- **Domain**: funnel
- **Description**: Drop-off rate from product view to add-to-cart and final purchase.
- **SQL File**: `src/models/marts/view_to_cart_funnel.sql`

## Cart Abandonment Rate
- **Domain**: funnel
- **Description**: Daily tracker of carts created against successful purchases.
- **SQL File**: `src/models/marts/cart_abandonment_rate.sql`

## Time To First Purchase
- **Domain**: funnel
- **Description**: Time elapsed from first view to an initial successful checkout.
- **SQL File**: `src/models/marts/time_to_first_purchase.sql`

## Hourly Conversion Heatmap
- **Domain**: temporal
- **Description**: Conversion rates mapped by hour of day and day of week.
- **SQL File**: `src/models/marts/hourly_conversion_heatmap.sql`

## Weekend Degradation
- **Domain**: temporal
- **Description**: Analysis of average sessions and revenue comparing weekends to weekdays.
- **SQL File**: `src/models/marts/weekend_degradation.sql`

## Time Of Day Aov Correlation
- **Domain**: temporal
- **Description**: Correlation between time of purchase mapping explicitly to AOV swings.
- **SQL File**: `src/models/marts/time_of_day_aov_correlation.sql`

## Anomaly Detection
- **Domain**: temporal
- **Description**: Rule-based model detecting 20% drops against a 7-day conversion average.
- **SQL File**: `src/models/alerts/anomaly_detection.sql`

