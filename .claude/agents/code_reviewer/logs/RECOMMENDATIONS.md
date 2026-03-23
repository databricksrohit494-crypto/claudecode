# Actionable Recommendations Summary

**Date:** 2026-03-24
**Review Scope:** 2 Python scripts in `.claude/skills/`

---

## Quick Reference: Issues by Severity

### 🔴 CRITICAL (Block deployment)
- [ ] `covert_to_parquet.py`: Rename file (typo)
- [ ] `covert_to_parquet.py`: Remove hardcoded absolute paths
- [ ] `visualize_data.py`: Refactor into functions (no functions currently)
- [ ] `visualize_data.py`: Remove hardcoded absolute path (Windows-specific)
- [ ] `visualize_data.py`: Add type hints (required by CLAUDE.md)

### 🟠 HIGH (Should fix before next release)
- [ ] `covert_to_parquet.py`: Improve exception handling (too generic)
- [ ] `covert_to_parquet.py`: Replace print() with logging module
- [ ] `visualize_data.py`: Add error handling for file operations
- [ ] `visualize_data.py`: Extract plotting code into reusable function
- [ ] `visualize_data.py`: Add comprehensive docstrings

### 🟡 MEDIUM (Improve quality)
- [ ] `covert_to_parquet.py`: Add CSV data validation
- [ ] `covert_to_parquet.py`: Create configuration management
- [ ] `visualize_data.py`: Add data quality checks before plotting
- [ ] `visualize_data.py`: Create configuration file
- [ ] Both: Update `pyproject.toml` with dependencies

### 🔵 LOW (Nice to have)
- [ ] `visualize_data.py`: Remove unused imports (`datetime`)
- [ ] `visualize_data.py`: Fix customer identifier inconsistency
- [ ] `covert_to_parquet.py`: Optimize file size calculation

---

## Detailed Fix Instructions

### File: `covert_to_parquet.py`

#### Fix #1: Rename File
```bash
# From: covert_to_parquet.py
# To:   convert_to_parquet.py
```
**Why:** Typo in filename is confusing and unprofessional.

---

#### Fix #2: Remove Hardcoded Paths
**Current (lines 92-93):**
```python
source_base = r".\.claude\skills\fetchAPI\data"
output_base = r".\.claude\skills\migrate\data"
```

**Recommended:**
```python
from pathlib import Path
import os

# Get root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONFIG = {
    "source_base": PROJECT_ROOT / ".claude" / "skills" / "fetchAPI" / "data",
    "output_base": PROJECT_ROOT / ".claude" / "skills" / "migrate" / "data",
}

def main(source_base: str | None = None, output_base: str | None = None) -> None:
    """
    Main function to orchestrate the conversion process.

    Args:
        source_base: Override default source base path
        output_base: Override default output base path
    """
    source_base = source_base or str(CONFIG["source_base"])
    output_base = output_base or str(CONFIG["output_base"])
    # ... rest of function
```

**Why:** Makes script portable, testable, and reusable across environments.

---

#### Fix #3: Improve Exception Handling
**Current (lines 85-86):**
```python
except Exception as e:
    print(f"  [ERR] Error converting {csv_file.name}: {str(e)}")
```

**Recommended:**
```python
except pd.errors.ParserError as e:
    logger.error(f"CSV parsing error in {csv_file.name}: {e}")
    # Continue with next file (recoverable error)
except (FileNotFoundError, PermissionError) as e:
    logger.error(f"File I/O error for {csv_file.name}: {e}")
    # Continue with next file (recoverable error)
except Exception as e:
    logger.error(f"Unexpected error converting {csv_file.name}: {e}")
    raise  # Re-raise to stop processing (unexpected error)
```

**Why:** Distinguishes recoverable errors from fatal ones; allows selective retries.

---

#### Fix #4: Replace print() with Logging
**Add at top of file:**
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

**Replace all print() calls:**
```python
# Before:
print(f"Found {len(csv_files)} CSV file(s) in {source_folder}")

# After:
logger.info(f"Found {len(csv_files)} CSV file(s) in {source_folder}")
```

**Why:** Enables logging to file, different verbosity levels, and proper timestamps.

---

#### Fix #5: Add Data Validation
**In convert_csv_to_parquet() function:**
```python
def convert_csv_to_parquet(...) -> None:
    # ... existing code ...
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)

            # Add validation
            if df.empty:
                logger.warning(f"CSV file {csv_file.name} is empty; skipping")
                continue

            # Check for completely empty columns
            if df.isnull().all().any():
                empty_cols = df.columns[df.isnull().all()].tolist()
                logger.warning(f"Dropping empty columns in {csv_file.name}: {empty_cols}")
                df = df.dropna(axis=1, how='all')

            # ... rest of conversion
```

**Why:** Catches data quality issues early; prevents silent failures.

---

### File: `visualize_data.py`

#### Fix #1: Add Module Docstring & Type Hints
**Current (lines 1-5):**
```python
"""
Data visualization and KPI analysis script.

Reads parquet files and generates KPIs and visualizations.
"""
```

**Recommended:**
```python
"""
Data visualization and KPI analysis script.

Reads CSV files from a data directory and generates KPI summaries and
visualizations (trend charts, aggregations by dimension).

This module is designed to be imported and used programmatically, not just
run as a standalone script. All functions accept configurable paths.

Example:
    python -c "from visualize_data import main; main()"

    Or use functions directly:
    from visualize_data import load_data, calculate_kpis
    data = load_data(Path("./data"))
    kpis = calculate_kpis(data["fact_sales"], data["fact_returns"])
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)
```

**Why:** Proper documentation, type hints enable IDE support and static analysis.

---

#### Fix #2: Refactor into Functions
**Extract data loading (lines 24-30):**
```python
def load_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """
    Load all required CSV files from data directory.

    Args:
        data_dir: Path to directory containing CSV files

    Returns:
        Dictionary mapping table names to DataFrames

    Raises:
        FileNotFoundError: If any required file is missing
        pd.errors.ParserError: If CSV parsing fails
    """
    required_files = {
        "dim_customer": "dim_customer.csv",
        "dim_date": "dim_date.csv",
        "dim_product": "dim_product.csv",
        "dim_store": "dim_store.csv",
        "fact_sales": "fact_sales.csv",
        "fact_returns": "fact_returns.csv",
    }

    data = {}
    for key, filename in required_files.items():
        filepath = Path(data_dir) / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Required file missing: {filepath}")

        try:
            data[key] = pd.read_csv(filepath)
            logger.info(f"Loaded {filename}: {len(data[key])} records")
        except pd.errors.ParserError as e:
            raise ValueError(f"Failed to parse {filename}: {e}") from e

    return data
```

**Extract KPI calculation (lines 49-63):**
```python
def calculate_kpis(
    fact_sales: pd.DataFrame,
    fact_returns: pd.DataFrame
) -> Dict[str, float]:
    """
    Calculate key performance indicators.

    Args:
        fact_sales: Sales fact table
        fact_returns: Returns fact table

    Returns:
        Dictionary of KPI values
    """
    total_sales = fact_sales["net_amount"].sum()
    total_returns = fact_returns["refund_amount"].sum()
    net_sales = total_sales - total_returns

    return {
        "total_sales": total_sales,
        "total_returns": total_returns,
        "net_sales": net_sales,
        "avg_sales_per_store": fact_sales.groupby("store_sk")["net_amount"].mean().mean(),
        "avg_sales_per_product": fact_sales.groupby("product_sk")["net_amount"].mean().mean(),
        "avg_sales_per_customer": fact_sales.groupby("customer_sk")["net_amount"].mean().mean(),
    }
```

**Extract generic visualization (consolidate lines 65-174):**
```python
def create_chart(
    data: pd.DataFrame,
    group_column: str,
    value_column: str,
    title: str,
    output_path: Path,
    chart_type: str = "bar",
    top_n: int | None = None,
    figsize: tuple = (12, 6),
    color: str = "#1f77b4",
) -> None:
    """
    Create and save a visualization.

    Args:
        data: DataFrame to visualize
        group_column: Column to group/aggregate by
        value_column: Column to sum/aggregate
        title: Chart title
        output_path: Path to save PNG file
        chart_type: "bar", "barh", or "line"
        top_n: Limit to top N groups (optional)
        figsize: Figure dimensions
        color: Color code for chart
    """
    grouped_data = data.groupby(group_column)[value_column].sum().sort_values(ascending=False)

    if top_n:
        grouped_data = grouped_data.head(top_n)

    if grouped_data.empty:
        logger.warning(f"No data for {title}; skipping visualization")
        return

    plt.figure(figsize=figsize)

    if chart_type == "bar":
        grouped_data.plot(kind="bar", color=color)
    elif chart_type == "barh":
        grouped_data.plot(kind="barh", color=color)
    elif chart_type == "line":
        plt.plot(grouped_data.index, grouped_data.values, linewidth=2, color=color)

    plt.title(title, fontsize=14, fontweight="bold")
    plt.xlabel(value_column)
    plt.ylabel(group_column)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    try:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        logger.info(f"Saved visualization: {output_path.name}")
    except IOError as e:
        logger.error(f"Failed to save {output_path.name}: {e}")
        raise
    finally:
        plt.close()
```

**Extract main orchestration (lines 1-177):**
```python
def main(
    data_dir: Path | str | None = None,
    output_dir: Path | str | None = None
) -> None:
    """
    Load data, calculate KPIs, and generate visualizations.

    Args:
        data_dir: Path to CSV data directory (uses default if None)
        output_dir: Path to save visualizations (uses default if None)
    """
    # Set defaults
    if data_dir is None:
        data_dir = Path("./.claude/skills/fetchAPI/data/latest")
    if output_dir is None:
        output_dir = Path("./.claude/skills/visualize/visualizations")

    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Setup visualization style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10

    # Load data
    logger.info("Loading data...")
    data = load_data(data_dir)

    # Calculate KPIs
    logger.info("Calculating KPIs...")
    kpis = calculate_kpis(data["fact_sales"], data["fact_returns"])

    logger.info("=== KPI Summary ===")
    for kpi_name, value in kpis.items():
        logger.info(f"{kpi_name}: ${value:,.2f}")

    # Create visualizations
    logger.info("Generating visualizations...")

    # Sales trend
    create_chart(
        data["fact_sales"].merge(data["dim_date"], on="date_sk"),
        group_column="date",
        value_column="net_amount",
        title="Sales Trend Over Time",
        output_path=output_dir / "sales_trend_over_time.png",
        chart_type="line",
        figsize=(14, 6),
        color="#1f77b4"
    )

    # ... generate remaining visualizations ...

    logger.info(f"Visualization complete! Saved to {output_dir}")
```

**Why:** Functions are testable, reusable, and can be documented properly.

---

#### Fix #3: Remove Hardcoded Paths
**Current (lines 14-15):**
```python
DATA_DIR = Path(r"e:\vscode\claudecode\.claude\skills\fetchAPI\data\2026-03-22_00-45-35")
OUTPUT_DIR = Path(r"e:\vscode\claudecode\.claude\skills\visualize\visualizations")
```

**Recommended:**
- Use configuration file (see Fix #4)
- Accept paths as function arguments (see refactored main())
- Use relative paths or environment variables

---

#### Fix #4: Create Configuration File
**Create `visualize_config.yaml`:**
```yaml
# Data pipeline configuration
data_pipeline:
  base_dir: ./.claude/skills
  fetch_data_dir: fetchAPI/data
  visualize_output_dir: visualize/visualizations

# Visualization settings
visualization:
  dpi: 300
  figsize: [12, 6]
  font_size: 10
  style: whitegrid

# Chart color palette
colors:
  sales: "#1f77b4"
  returns: "#d62728"
  stores: "#2ca02c"
  products: "#d62728"
  customers: "#ff7f0e"

# Charts to generate
charts:
  sales_trend:
    title: "Sales Trend Over Time"
    chart_type: line
    group_by: date
    value_column: net_amount
  sales_by_store:
    title: "Total Sales by Store"
    chart_type: bar
    group_by: store_name
    value_column: net_amount
```

**Load configuration:**
```python
import yaml
from pathlib import Path

def load_config(config_path: Path = Path("visualize_config.yaml")) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# In main():
config = load_config()
data_dir = Path(config["data_pipeline"]["fetch_data_dir"])
```

**Why:** Decouples configuration from code; easier to adjust for different environments.

---

#### Fix #5: Add Error Handling & Validation
**Add validation after data load:**
```python
def validate_data(data: Dict[str, pd.DataFrame]) -> None:
    """
    Validate data integrity and quality.

    Raises:
        ValueError: If data is invalid or incomplete
    """
    # Check required columns
    fact_sales_cols = {"date_sk", "store_sk", "product_sk", "customer_sk", "net_amount"}
    if not fact_sales_cols.issubset(set(data["fact_sales"].columns)):
        raise ValueError(f"fact_sales missing columns: {fact_sales_cols - set(data['fact_sales'].columns)}")

    # Check for excessive nulls
    for table_name, df in data.items():
        null_pct = df.isnull().sum() / len(df)
        if (null_pct > 0.5).any():
            cols_with_nulls = null_pct[null_pct > 0.5].index.tolist()
            logger.warning(f"{table_name} has >50% nulls in: {cols_with_nulls}")
```

**Why:** Fails fast with clear error messages instead of producing bad visualizations.

---

## Testing Strategy

### For `covert_to_parquet.py`
```python
# tests/test_covert_to_parquet.py
import pytest
from pathlib import Path
import pandas as pd
from convert_to_parquet import get_latest_folder, convert_csv_to_parquet

def test_get_latest_folder(tmp_path):
    (tmp_path / "2026-01-01").mkdir()
    (tmp_path / "2026-03-24").mkdir()
    name, path = get_latest_folder(str(tmp_path))
    assert name == "2026-03-24"

def test_convert_csv_with_valid_data(tmp_path):
    # Create test CSV
    csv_path = tmp_path / "test.csv"
    pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}).to_csv(csv_path, index=False)

    # Convert
    output_path = tmp_path / "output"
    convert_csv_to_parquet(str(tmp_path), str(output_path), "test_folder")

    # Verify
    assert (output_path / "test_folder" / "test.parquet").exists()
```

### For `visualize_data.py`
```python
# tests/test_visualize_data.py
import pytest
from pathlib import Path
import pandas as pd
from visualize_data import load_data, calculate_kpis

def test_load_data_creates_all_tables(tmp_path):
    # Create mock CSV files
    for filename in ["dim_customer.csv", "fact_sales.csv", ...]:
        pd.DataFrame({"id": [1, 2]}).to_csv(tmp_path / filename, index=False)

    data = load_data(tmp_path)
    assert len(data) == 6

def test_calculate_kpis(sample_data):
    kpis = calculate_kpis(sample_data["fact_sales"], sample_data["fact_returns"])
    assert kpis["net_sales"] == kpis["total_sales"] - kpis["total_returns"]
```

---

## Dependency Updates

**Update `pyproject.toml`:**
```toml
[project]
name = "claude-data-pipeline"
version = "0.1.0"
requires-python = ">=3.9"

[project.dependencies]
pandas = ">=2.0.0"
pyarrow = ">=14.0.0"
matplotlib = ">=3.7.0"
seaborn = ">=0.12.0"
pyyaml = ">=6.0"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
]
```

---

## Summary of Changes

| File | Changes | Effort | Impact |
|------|---------|--------|--------|
| `covert_to_parquet.py` | Rename, refactor paths, improve exceptions, add logging, add validation | 2-3 hours | High |
| `visualize_data.py` | Add functions, refactor, remove hardcodes, add config, add error handling | 4-5 hours | High |
| Both | Add type hints, docstrings, testing, dependency management | 2-3 hours | High |

**Total Estimated Effort:** 8-11 hours
**Priority:** CRITICAL (before next deployment)

---

**End of Recommendations**
