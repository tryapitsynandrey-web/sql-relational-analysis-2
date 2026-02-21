## 🏗 Architecture & Design Philosophy

This project strictly adheres to modern Analytics Engineering principles (analogous to dbt workflows). Raw event data (views, carts, purchases) is systematically transformed into decision-grade metrics through a layered architecture.

**The Golden Rule:** The UI is strictly a presentation layer. Absolutely zero DataFrames aggregations, Pandas `.mean()` calls, or Python math exist in the presentation layer. 

**Stateless UI / Logic-Heavy DB Split:**
- **Data Layer (`src/models/marts/`)**: 30+ complex `.sql` files leverage DuckDB to perform all mathematical transformations, cohort clustering, and anomaly detection using Common Table Expressions (CTEs) and Window Functions.
- **Orchestration Layer (`src/core/`)**: Python acts exclusively as a transport protocol, managing connection pooling, automated testing, and execution state.
- **Presentation Layer (`src/ui/`)**: Streamlit and Plotly blindly render the pre-aggregated SQL sets.

*Diagram Placeholder: [System Architecture Schematic illustrating DuckDB OLAP processing feeding Streamlit]*

---

## 🛠 Core Feature Matrix

The engine processes raw, timestamped user telemetry into 35+ measurable outputs across 4 distinct business domains:

| Category | Key Metrics Handled | Technical Implementation |
| :--- | :--- | :--- |
| **Temporal Trends** | Hourly Conversion Heatmaps, Weekend Degradation | `EXTRACT(DAYOFWEEK FROM ts)`, `AVG()` grouped by hour and day arrays. |
| **Behavioral Funnels** | View-to-Cart-to-Purchase, Time-to-First-Purchase, Cart Abandonment | Multi-stage CTEs calculating drop-off percentages; aggregate counts divided by upper-funnel baseline constants. |
| **Revenue Economics** | Average Order Value (AOV), Customer Lifetime Value (LTV), Category Margin | Aggregated sums partitioned by synthetic monthly cohorts. |
| **Rule-Based Anomalies** | Conversion Drop Detection (20%+ off 7D MA) | Window Functions computing 7-day trailing moving averages compared against discrete daily outputs. |

---

## 💻 Technical Deep Dive

This platform demonstrates senior-level data modeling and optimization techniques:

- **Advanced SQL Constructs:**
  - **Window Functions:** Heavy utilization of `LEAD()`, `LAG()`, and `NTILE(4)` for RFM segmentation (Recency, Frequency, Monetary value).
  - **Self-Joins for Market Baskets:** Calculated product co-occurrence strictly in SQL. Prevented Cartesian explosions using bounding inequalities (`a.product_id < b.product_id`) grouped strictly by absolute `session_id`.
  - **CTE-Based Funnel Math:** Ensured division-by-zero protection (`NULLIF()`) during multi-stage view-to-purchase funnel aggregations.
- **Performance Optimizations:**
  - **Read-Only Concurrency:** The `DBClient` instantiates DuckDB locally passing `read_only=True` natively avoiding file locking failures during multi-threaded Streamlit user access.
  - **Smart UI Caching:** Leveraged Streamlit's native `@st.cache_data` decorated via an injected `with_cache` wrapper. Crucially utilized `_self` parameter assignments to bypass Streamlit hashing algorithms attempting to serialize the unhashable `MetricEngine` class context, eliminating `SerializationExceptions`.

---

## 📈 Interactive Insights

The dashboard doesn't just show charts; it interprets them.

The **Executive Summary** tab utilizes Python f-strings to dynamically inject pre-calculated SQL constants (e.g., `df.iloc[0]['drop_percentage']`) directly into hardcoded business recommendations. This bridges the gap between raw data analysis and actionable operational directives—an essential requirement for executive stakeholders.

*Visual Placeholder: [Screenshot of Plotly Density Heatmap plotting Conversion Rate by Hour and Day]*

---

## 🚀 Getting Started (Reproducibility)

The environment is designed for zero-configuration, deterministic local setups.

**1. Clone the Repository:**
```bash
git clone https://github.com/andrewshwarts/sql-relational-analysis-2.git
cd sql-relational-analysis-2
```

**2. Hydrate the Environment:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Seed the Analytics Database:**
*Generates 15,000 synthetically modeled e-commerce interactions mimicking realistic market baskets and funnel abandonments.*
```bash
python scripts/seed_database.py
```

**4. Launch the Engine:**
```bash
python start_analysis.py
```

---

## 🔬 Developer Notes

- **Assumptions:** The synthetic data generation (`scripts/seed_database.py`) actively injects temporal latency and conditional probabilities (e.g., 30% view-to-cart rate) intended to mimic standard mid-market retail conversion distributions.
- **Limitations:** The platform is currently bound to local DuckDB execution. Scaling to TB-scale event telemetry would require migrating the SQL models to dbt and transitioning the execution engine to Snowflake or BigQuery.
- **Edge Cases Handled:** 
  - Division-by-zero errors in funnel math are caught natively in SQL. 
  - Time-series charts utilize fixed-axis limits (whole integers for month counts) explicitly passed into Plotly functions (`dtick=1`) to prevent float interpolation artifacts.

---

## 🎯 Skills & Certification Mapping

| Demonstrated Skill | Evidence in Codebase |
| :--- | :--- |
| **Analytics Engineering** | Strict separation of stateless UI (Streamlit) from Stateful Logic (DuckDB models). |
| **Data Modeling** | Fact/Dim table creation (synthesized) feeding complex denormalized aggregations. |
| **Performance Tuning** | Query optimization bypassing Cartesian explosions; implemented `st.cache_data` caching to circumvent runtime redundant SQL polling. |
| **QA / Validation** | Multi-tier pytest suite evaluating DB locking, null-value handling, and SQL mathematical assertions. |
