# Airflow Project - DAGs Documentation

This project contains Apache Airflow DAGs (Directed Acyclic Graphs) for data pipeline orchestration. The DAGs demonstrate asset-based scheduling and data transformation workflows.

---

## Project Structure

```
Airflow_Project/
├── dags/
│   ├── data_fetch.py       # Producer DAG - fetches and transforms data
│   └── data_report.py      # Consumer DAG - generates reports from fetched data
└── README.md               # This documentation
```

---

## DAGs Overview

### 1. data_fetch.py

**Purpose:** Fetches weather data from an external API, transforms it, and materializes it as an Airflow Asset.

**DAG Name:** `data_fetch`

**Workflow:**
```
prepare_storage() → fetch_api_data() → transform_data() → materialize_asset()
```

**Tasks:**

| Task | Description | Output |
|------|-------------|--------|
| `prepare_storage()` | Creates the directory structure for storing data | Path: `/opt/airflow/data/weather_report.json` |
| `fetch_api_data()` | Simulates an API call and returns weather data | `{"city": "New York", "temp": 22, "unit": "C"}` |
| `transform_data(raw_data)` | Adds metadata and processing information to the raw data | Enhanced data with `processed_at` and `status` fields |
| `materialize_asset(final_data, path)` | Writes the final data to a JSON file and creates an asset outlet | Asset: `weather_data_asset` |

**Asset Produced:**
- **Name:** `weather_data_asset`
- **URI:** `file:///opt/airflow/data/weather_report.json`
- **Type:** JSON file containing weather information

**Key Features:**
- Uses Airflow decorators (`@dag`, `@task`)
- Implements asset-based scheduling (outlet)
- Demonstrates data transformation pipeline
- Creates a reusable asset for downstream DAGs

---

### 2. data_report.py

**Purpose:** Consumes the weather data asset produced by `data_fetch` DAG and generates analysis/reports.

**DAG Name:** `data_report`

**Workflow:**
```
read_asset()
```

**Tasks:**

| Task | Description | Input |
|------|-------------|-------|
| `read_asset()` | Reads the weather data asset and prints analysis | Consumes `weather_data_asset` |

**Scheduling:**
- **Trigger:** Scheduled to run whenever the `weather_data_asset` is updated
- **Schedule:** `schedule=[weather_data_asset]` (Asset-based scheduling)

**Key Features:**
- Uses asset-based scheduling (depends on `data_fetch` DAG)
- Reads and analyzes data from the produced asset
- Demonstrates consumer-producer relationship between DAGs

---

## Workflow Relationships

```
┌──────────────────────┐
│   data_fetch DAG     │
├──────────────────────┤
│ 1. Prepare Storage   │
│ 2. Fetch API Data    │
│ 3. Transform Data    │
│ 4. Materialize Asset │
│      (Outlet)        │
└──────────────────────┘
           │
           │ weather_data_asset
           ▼
┌──────────────────────┐
│  data_report DAG     │
├──────────────────────┤
│    Read Asset        │
│    Generate Report   │
└──────────────────────┘
```

---

## Asset-Based Scheduling

This project leverages **Asset-Based Scheduling**, a feature in Apache Airflow that allows DAGs to be triggered based on asset creation/updates rather than time-based schedules.

**How it works:**
1. `data_fetch` DAG produces a weather data asset
2. `data_report` DAG automatically triggers when the asset is updated
3. This creates a natural dependency between DAGs without explicit trigger rules

---

## Data Flow

### Input
- Simulated weather API call returning:
  ```json
  {
    "city": "New York",
    "temp": 22,
    "unit": "C"
  }
  ```

### Processing
1. **Fetch:** Retrieve raw weather data
2. **Transform:** Add metadata (processing timestamp and status)
3. **Materialize:** Save transformed data to persistent storage

### Output
- **Location:** `/opt/airflow/data/weather_report.json`
- **Format:** JSON file
- **Content:**
  ```json
  {
    "city": "New York",
    "temp": 22,
    "unit": "C",
    "processed_at": "2026-03-24T10:30:45.123456",
    "status": "cleansed"
  }
  ```

---

## Configuration

**Airflow Version:** Uses modern Airflow SDK decorators
- `@dag`: Decorator for DAG definition
- `@task`: Decorator for individual tasks
- Assets: For dependency management

**Storage Path:** `/opt/airflow/data/`

**File Format:** JSON

---

## Running the DAGs

### Prerequisites
- Apache Airflow installed and configured
- Required directories exist or can be created by `prepare_storage()`
- JSON library available

### Execution Steps

1. **Start Airflow:**
   ```bash
   airflow webserver --port 8080
   airflow scheduler
   ```

2. **Trigger data_fetch DAG:**
   - Via UI: Enable and manually trigger the DAG
   - Via CLI: `airflow dags trigger data_fetch`

3. **Monitor data_report DAG:**
   - Automatically triggers when `weather_data_asset` is updated
   - Monitor via Airflow UI for completion

---

## Error Handling

- **File System Errors:** `prepare_storage()` uses `exist_ok=True` to handle directory creation safely
- **Data Validation:** Add validation tasks if data format consistency is critical
- **Asset Dependencies:** Ensure `data_fetch` completes successfully before `data_report` runs

---

## Future Enhancements

- Replace simulated API call with actual weather API integration
- Add error handling and retry logic
- Implement data validation and quality checks
- Add logging and monitoring
- Extend to multiple data sources
- Implement data archival strategy

---

## Notes

- This is a simplified demonstration of asset-based scheduling
- The `fetch_api_data()` task currently returns hardcoded data
- File paths assume running in an Airflow container/environment
- Real-world implementation would include exception handling and data validation

---

*Last Updated: 2026-03-24*
