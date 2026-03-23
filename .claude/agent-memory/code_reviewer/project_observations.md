---
name: Project Structure and Data Pipeline Observations
description: Understanding of the project's data pipeline structure, naming conventions, and architectural patterns
type: project
---

## Project Structure

The project appears to be a data pipeline with three main skill modules:

```
.claude/skills/
├── fetchAPI/
│   └── data/
│       └── YYYY-MM-DD_HH-MM-SS/  (datetime-named folders)
│           ├── dim_customer.csv
│           ├── dim_date.csv
│           ├── dim_product.csv
│           ├── dim_store.csv
│           ├── fact_sales.csv
│           └── fact_returns.csv
├── migrate/
│   ├── scripts/
│   │   └── covert_to_parquet.py  (note: typo in filename)
│   └── data/
│       └── YYYY-MM-DD_HH-MM-SS/  (mirrored structure)
│           └── *.parquet files
└── visualize/
    ├── scripts/
    │   └── visualize_data.py
    └── visualizations/
        └── *.png files
```

---

## Data Schema Pattern

The project uses a **star schema** (fact/dimension pattern) common in data warehousing:

### Dimension Tables (Slowly Changing Dimensions)
- `dim_customer`: Customer attributes (includes `customer_sk`, `last_name`, ...)
- `dim_date`: Date dimension (includes `date_sk`, `date`, ...)
- `dim_product`: Product attributes (includes `product_sk`, `product_name`, ...)
- `dim_store`: Store attributes (includes `store_sk`, `store_name`, ...)

### Fact Tables (Transactional Data)
- `fact_sales`: Sales transactions (keys: `date_sk`, `store_sk`, `product_sk`, `customer_sk`, `net_amount`)
- `fact_returns`: Return transactions (keys: `date_sk`, `store_sk`, `product_sk`, `sales_id`, `refund_amount`)

**Note:** `fact_returns` uses `sales_id` as a foreign key to `fact_sales`, not direct customer_sk

---

## Pipeline Flow

1. **Fetch** → CSV files extracted to `.claude/skills/fetchAPI/data/YYYY-MM-DD_HH-MM-SS/`
2. **Migrate** → Convert CSV to Parquet format (same folder structure in migrate/data/)
3. **Visualize** → Generate KPI dashboards and visualizations from CSV data

---

## Data Pipeline Issues Observed

1. **Duplicate dimension table joins in visualize_data.py**:
   - `fact_returns` joins to `dim_customer` via `fact_sales` intermediate, not direct
   - This may introduce data quality issues if sales_id relationship is inconsistent

2. **Missing primary/foreign key validation**:
   - No checks for referential integrity
   - No validation that all foreign keys exist in dimension tables

3. **Datetime folder naming format**:
   - Format: `YYYY-MM-DD_HH-MM-SS` (e.g., `2026-03-22_00-45-35`)
   - Scripts rely on lexicographic ordering for "latest" (works but fragile)
   - Consider using ISO 8601 timestamps or numeric sorting for robustness

---

## Development Environment Assumptions

- **Windows OS** (evidenced by `r"e:\vscode\claudecode"` hardcoded paths)
- **Local development**: All paths are local filesystem, not cloud storage
- **Single-user workflow**: No multi-user locking or concurrency considerations
- **Test data**: Size not specified; scripts don't optimize for large datasets

---

## Naming Conventions Observed

1. **Table/Column Names**: Snake_case (SQL-style)
   - `dim_customer`, `fact_sales`, `customer_sk`, `date_sk`

2. **Foreign Key Pattern**: `{table}_sk` (surrogate key)
   - `customer_sk`, `date_sk`, `product_sk`, `store_sk`
   - Consistent across all fact/dimension tables

3. **File Naming**: Snake_case CSV/Parquet files
   - `dim_customer.csv`, `fact_sales.parquet`

4. **Function Naming** (CLAUDE.md requirement): Should be `camelCase`
   - Current scripts use `snake_case` (standard Python) — may need clarification

---

## Performance Observations

1. **Memory efficiency not optimized**:
   - All CSVs loaded into memory; no chunking for large files
   - Multiple copies of data during merges
   - Could benefit from parquet use (compress, lazy loading)

2. **Visualization generation**:
   - 8 separate matplotlib calls (could be batched)
   - No caching of intermediate merged datasets
   - File I/O not optimized

3. **Datetime column handling**:
   - Dates stored as strings in CSV (not datetime objects)
   - No type conversion before plotting (may affect sorting/filtering)

---

## Data Quality Concerns

1. **Returns to Sales Linkage**:
   - `fact_returns.sales_id` → `fact_sales.sales_id`
   - But `fact_returns` also has dimension keys; possible duplication/inconsistency

2. **Missing Null Handling**:
   - No documentation of nullable columns
   - Visualization scripts don't validate data quality before plotting

3. **Customer Identification**:
   - `visualize_data.py` uses `last_name` as customer identifier (line 109, 164)
   - Non-unique identifier; multiple customers may share last names
   - Should use `customer_sk` or `customer_id` instead

---

## Recommendations for Pipeline Evolution

1. **Create configuration file** for data paths instead of hardcoding
2. **Add data validation script** to check schema, referential integrity, completeness
3. **Standardize datetime handling** — convert to datetime objects in load step
4. **Create generic merge utility** to avoid duplication
5. **Add logging throughout pipeline** for debugging and monitoring
6. **Create modular visualization library** for reuse across projects
7. **Document schema** (expected columns, types, nullable fields)
8. **Consider adding timestamp tracking** for data lineage (when data was fetched/processed)

---

## Next Project Tasks

Based on observations:
1. Fix filename typo: `covert_to_parquet.py` → `convert_to_parquet.py`
2. Refactor `visualize_data.py` into functions (critical for maintainability)
3. Add configuration management for all hardcoded paths
4. Create schema validation layer before processing
5. Document data relationships and assumptions
