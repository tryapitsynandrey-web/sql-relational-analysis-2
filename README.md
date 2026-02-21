# SQL Relational Analysis v2

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit_1.31.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas_2.2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB_0.10.0-FFF000?style=for-the-badge)

## Description

The SQL Relational Analysis project is a specialized E-Commerce Behavioral Analytics pipeline and dashboard. It utilizes a SQL-first approach to process over 30 interconnected metrics, orchestrated by a highly structured metric engine written in Python. Utilizing DuckDB as its high-performance local analytical database and Streamlit for the user interface, it provides comprehensive insights into revenue, user behavioral retention, action funnels, temporal trends, and metric dependencies.

## Architecture Overview

The system strictly decouples analytical modeling and display interfaces, structured across the following layers:

- **UI (`src/ui/`)**: A Streamlit application rendering diverse tabs (`executive_summary`, `revenue_tab`, `behavior_tab`, etc.) based on data emitted by the metric engine.
- **Core (`src/core/`)**: The business logic orchestration layer, primarily through the `MetricEngine` that reads from the `metrics.yaml` configuration and dynamically delegates SQL query execution.
- **DB (`src/db/`)**: The storage interface (`DBClient`), mapping queries onto the embedded DuckDB database file.
- **Models (`src/models/`)**: Structured analytical domains (e.g., `staging`, `marts`, `alerts`), providing the precise SQL transformations orchestrated by the core.
- **Utils (`src/utils/`)**: General operations including TTL-based Dataframe cache (`cache_manager.py`), structured logging, export management, and specific formatters.

## Features

- **SQL-First Metric Configuration**: Dynamic evaluation of SQL files defined declaratively in `config/metrics.yaml`.
- **E-Commerce Dashboard**: Includes segmented tabs for Revenue & Economics, User Behavior & Retention, Funnels, Temporal properties, and Metric Dependencies.
- **Embedded Database Approach**: Seamless integration using DuckDB for direct query execution unburdened by external database network latency.
- **Read-Only Scaling**: The database client conditionally uses read-only connections to prevent file locks during concurrent Streamlit dashboard sessions.
- **In-Memory Caching**: TTL-defined data caching directly attached to metric retrieval to handle complex view recreations efficiently.

## Project Structure

```
├── .gitattributes
├── .gitignore
├── METRICS_DICTIONARY.md
├── Makefile
├── config/
│   ├── metrics.yaml
│   └── settings.yaml
├── data/
│   ├── 2019-Nov.csv
│   ├── 2019-Oct.csv
│   └── analytics.db
├── requirements.txt
├── scripts/
│   ├── generate_docs.py
│   ├── generate_report.py
│   └── seed_database.py
├── src/
│   ├── core/
│   ├── db/
│   ├── main.py
│   ├── models/
│   ├── ui/
│   └── utils/
├── start_analysis.py
└── tests/
```

## Installation

### Local

1. Verify that `python3` (with `venv` support) is installed.
2. Initialize the virtual environment and install dependencies via the provided Makefile:
   ```bash
   make install
   ```

### Docker

Not supported in this repository.

## Usage

### CLI

The repository maintains robust programmatic operations by directly invoking scripts or utilizing Make commands:

- **Generate Documentation**: `make docs`
- **Execute Metric Export**: `make export`
- **Run the Test Suite**: `make test`
- **Seed the Database**: `.venv/bin/python scripts/seed_database.py`

### Web

Initialize the interactive Streamlit dashboard:

Using the Makefile:
```bash
make run
```

Or, directly executing the python wrapper:
```bash
.venv/bin/python start_analysis.py
```

## Data Storage

Data is analyzed out-of-core and entirely locally using DuckDB. The embedded database resides at `data/analytics.db`. It interacts directly with the static data ingestion files (`2019-Oct.csv`, `2019-Nov.csv`), pulling in behavioral events for compilation. 

## Configuration

Configuration is managed natively via YAML files located in `config/`:
- **`settings.yaml`**: Standard application properties, debugging defaults, and database connection paths.
- **`metrics.yaml`**: The critical mapping of metric namespaces to backend execution logic, specifying the strict paths to executed `.sql` scripts.

## Development Notes

- **Testing**: Tests are grouped functionally under the `tests/` directory (e.g., `test_core.py`, `test_metric_engine.py`, `test_sql_models.py`) and engineered for pytest. Tests may require write access to the database to construct valid schema preconditions.
- **Dependency Sandboxing**: All runtime commands defined within the Makefile inherently use the environment bound isolated to `.venv/bin/`.

## Limitations & Assumptions

- **Python Versioning**: The explicit Python major and minor versions are omitted from `requirements.txt` and only broadly invoked via `python3`. While generally compatible, functionality assumes a relatively modern Python 3.9+ environment.
- **Database Mutex Issues**: Concurrency is limited strictly to reads by default due to standard DuckDB file-locking implementations. The dashboard explicitly instantiates the DuckDB connections as `read_only=True` to prevent lock crashes from parallel Web UI consumers. Write functions should be siloed.
- **Data Availability**: The local analytics process operates on the precise assumption that properly formatted `2019-Nov.csv` and `2019-Oct.csv` data manifests natively in the `/data` directory prior to initialization or testing. 
- **Scale Requirements**: Despite robust out-of-core processing by DuckDB, running the application on commodity hardware relies on the system successfully executing queries over datasets potentially exceeding 14GB without memory exhaustion.

## License

Not specified
