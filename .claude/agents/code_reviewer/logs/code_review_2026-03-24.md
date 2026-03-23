# Code Review Report: Python Scripts in `.claude/skills`

**Date:** 2026-03-24
**Reviewer:** Claude Code
**Files Reviewed:** 2 Python scripts

---

## File 1: `.claude/skills/migrate/scripts/covert_to_parquet.py`

### Overall Assessment
**Grade: B+**

This script demonstrates good structure with well-organized functions, proper error handling, and adequate documentation. However, there are opportunities for improvement in type hints, path handling, and configuration management.

---

### Strengths

1. **Clear Module Structure**: Functions are logically separated with a single responsibility principle.
2. **Type Hints**: Present in function signatures (lines 13, 40-44).
3. **Error Handling**: Catches exceptions gracefully with informative output (lines 85-86, 112-115).
4. **Path Handling**: Uses `pathlib.Path` for cross-platform compatibility (good practice).
5. **User Feedback**: Provides clear console output about progress and results.
6. **Documentation**: Module-level docstring and function docstrings present.

---

### Issues & Recommendations

#### 1. **Filename Typo (Critical)**
- **Line 1-6:** Script is named `covert_to_parquet.py` but should be `convert_to_parquet.py`
- **Issue:** Typo in filename is misleading and unprofessional
- **Fix:** Rename file to `convert_to_parquet.py`

#### 2. **Hardcoded Paths (High Priority)**
- **Lines 92-93:** Paths are hardcoded with Windows-specific raw strings
```python
source_base = r".\.claude\skills\fetchAPI\data"
output_base = r".\.claude\skills\migrate\data"
```
- **Issue:** Not cross-platform, difficult to reuse, violates DRY principle
- **Recommendation:**
```python
from pathlib import Path
import sys

# Get the root directory dynamically
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # Adjust based on structure
CONFIG = {
    "source_base": PROJECT_ROOT / ".claude" / "skills" / "fetchAPI" / "data",
    "output_base": PROJECT_ROOT / ".claude" / "skills" / "migrate" / "data",
}

def main(source_base: str | None = None, output_base: str | None = None):
    """Main function with configurable paths."""
    source_base = source_base or str(CONFIG["source_base"])
    output_base = output_base or str(CONFIG["output_base"])
    # ... rest of function
```

#### 3. **Missing Return Type Annotation**
- **Line 40-44:** `convert_csv_to_parquet()` has incomplete return type
```python
def convert_csv_to_parquet(...) -> None:  # ✓ Good
```
- **Issue:** Already correct, but recommend all functions have explicit return types
- **Status:** This is fine

#### 4. **Incomplete Exception Handling**
- **Lines 71-86:** Generic `Exception` catch is too broad
```python
except Exception as e:
    print(f"  [ERR] Error converting {csv_file.name}: {str(e)}")
```
- **Issue:** Silently continues on any error; doesn't distinguish between read/write/data errors
- **Recommendation:**
```python
except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
    print(f"  [ERR] CSV parsing error in {csv_file.name}: {str(e)}")
except IOError as e:
    print(f"  [ERR] File I/O error for {csv_file.name}: {str(e)}")
except Exception as e:
    print(f"  [ERR] Unexpected error converting {csv_file.name}: {str(e)}")
    raise  # Re-raise to indicate unexpected failure
```

#### 5. **No Logging Mechanism**
- **Issue:** Uses `print()` instead of proper logging module
- **Recommendation:**
```python
import logging

logger = logging.getLogger(__name__)

# In main():
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger.info(f"Found {len(csv_files)} CSV file(s)")
logger.error(f"Error converting {csv_file.name}: {str(e)}")
```

#### 6. **Missing Data Validation**
- **Lines 73-80:** No validation of CSV content or data quality
- **Recommendation:**
```python
def convert_csv_to_parquet(...) -> None:
    # ... existing code ...
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)

            # Add validation
            if df.empty:
                logger.warning(f"CSV file {csv_file.name} is empty, skipping")
                continue

            if df.isnull().all().any():
                logger.warning(f"CSV file {csv_file.name} has empty columns")
                # Decide: drop columns or skip file

            # ... rest of conversion
```

#### 7. **Hard-coded Engine Parameter**
- **Line 80:** `engine="pyarrow"` is hardcoded
- **Issue:** Less flexible; pyarrow may not be installed
- **Recommendation:**
```python
def convert_csv_to_parquet(..., engine: str = "pyarrow") -> None:
    # Allow caller to specify or fall back
    try:
        df.to_parquet(parquet_path, engine=engine, index=False)
    except ImportError:
        logger.warning(f"Engine {engine} not available, using default")
        df.to_parquet(parquet_path, index=False)
```

#### 8. **No Dependency Documentation**
- **Issue:** No `requirements.txt` or `pyproject.toml` specifying pandas/pyarrow versions
- **Recommendation:** Create or update project dependencies file with:
```
pandas>=2.0.0
pyarrow>=14.0.0
```

#### 9. **Inefficient File Size Calculation**
- **Lines 83:** Calls `.stat()` after file creation (extra I/O)
- **Recommendation:**
```python
# After saving:
file_size_kb = parquet_path.stat().st_size / 1024
print(f"  [OK] {csv_file.name} -> {parquet_filename}")
print(f"    Shape: {df.shape} | Size: {file_size_kb:.2f} KB")
```
This is acceptable but could be optimized by tracking bytes written.

#### 10. **Missing Type Hint for Generic Return**
- **Line 13:** `tuple[str, str]` is correct for Python 3.9+, but consider adding `Optional` if needed
```python
from typing import Tuple  # For compatibility with older Python

def get_latest_folder(source_path: str) -> Tuple[str, str]:
    # ... correct already in code
```

---

### Code Quality Score

| Criterion | Score | Notes |
|-----------|-------|-------|
| Structure | 8/10 | Well-organized; minor issues |
| PEP 8 Compliance | 7/10 | Good; hardcoded paths reduce portability |
| Type Hints | 8/10 | Present; could be more complete |
| Documentation | 8/10 | Good docstrings; missing config docs |
| Error Handling | 6/10 | Basic; too generic exceptions |
| Maintainability | 6/10 | Hardcoded paths; no logging |
| Performance | 7/10 | Acceptable; minor optimizations possible |

---

---

## File 2: `.claude/skills/visualize/scripts/visualize_data.py`

### Overall Assessment
**Grade: D+**

This script has significant structural and quality issues that prevent it from being maintainable or reusable. While it accomplishes its goal, it violates multiple best practices and project standards.

---

### Issues & Recommendations

#### 1. **Script is Not Modular (Critical)**
- **Lines 1-177:** Entire script is procedural with no functions
- **Issue:** Cannot be reused, tested, or debugged easily; violates PEP 8 and project standards
- **Impact:** Very low maintainability; impossible to unit test
- **Fix:** Refactor into functions:

```python
"""Data visualization and KPI analysis script."""

import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

def load_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load all CSV files from data directory."""
    data = {}
    files = {
        "dim_customer": "dim_customer.csv",
        "dim_date": "dim_date.csv",
        "dim_product": "dim_product.csv",
        "dim_store": "dim_store.csv",
        "fact_sales": "fact_sales.csv",
        "fact_returns": "fact_returns.csv",
    }

    for key, filename in files.items():
        try:
            data[key] = pd.read_csv(data_dir / filename)
            logger.info(f"Loaded {filename}: {len(data[key])} records")
        except FileNotFoundError as e:
            logger.error(f"Missing file: {filename}")
            raise

    return data

def merge_sales_data(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Merge fact_sales with dimension tables."""
    sales_data = data["fact_sales"].copy()
    for dim_name in ["dim_date", "dim_store", "dim_product", "dim_customer"]:
        key_col = f"{dim_name.split('_')[1]}_sk"
        sales_data = sales_data.merge(
            data[dim_name],
            left_on=key_col,
            right_on=key_col,
            how="left"
        )
    return sales_data

def calculate_kpis(sales_data: pd.DataFrame, returns_data: pd.DataFrame) -> Dict[str, float]:
    """Calculate key performance indicators."""
    kpis = {
        "total_sales": sales_data["net_amount"].sum(),
        "total_returns": returns_data["refund_amount"].sum(),
        "avg_sales_per_store": sales_data.groupby("store_sk")["net_amount"].mean().mean(),
        "avg_sales_per_product": sales_data.groupby("product_sk")["net_amount"].mean().mean(),
        "avg_sales_per_customer": sales_data.groupby("customer_sk")["net_amount"].mean().mean(),
    }
    kpis["net_sales"] = kpis["total_sales"] - kpis["total_returns"]
    return kpis

def plot_sales_trend(sales_data: pd.DataFrame, output_dir: Path) -> None:
    """Create sales trend visualization."""
    sales_by_date = sales_data.groupby("date")["net_amount"].sum().reset_index()
    sales_by_date = sales_by_date.sort_values("date")

    plt.figure(figsize=(14, 6))
    plt.plot(sales_by_date["date"], sales_by_date["net_amount"], linewidth=2, color="#1f77b4")
    plt.title("Sales Trend Over Time", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Sales Amount ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "sales_trend_over_time.png", dpi=300, bbox_inches="tight")
    plt.close()

# ... more visualization functions ...

def main(data_dir: Path | str = None, output_dir: Path | str = None) -> None:
    """Main function to orchestrate visualizations."""
    # Use provided paths or defaults
    if data_dir is None:
        data_dir = Path(r"e:\vscode\claudecode\.claude\skills\fetchAPI\data\2026-03-22_00-45-35")
    if output_dir is None:
        output_dir = Path(r"e:\vscode\claudecode\.claude\skills\visualize\visualizations")

    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.INFO)

    # Load data
    data = load_data(data_dir)

    # Merge and calculate
    sales_data = merge_sales_data(data)
    kpis = calculate_kpis(data["fact_sales"], data["fact_returns"])

    # Print KPIs
    for kpi_name, value in kpis.items():
        logger.info(f"{kpi_name}: ${value:,.2f}")

    # Create visualizations
    plot_sales_trend(sales_data, output_dir)
    # ... call other visualization functions ...

if __name__ == "__main__":
    main()
```

#### 2. **Hardcoded, Absolute Paths (Critical)**
- **Lines 14-15:** Absolute hardcoded paths
```python
DATA_DIR = Path(r"e:\vscode\claudecode\.claude\skills\fetchAPI\data\2026-03-22_00-45-35")
OUTPUT_DIR = Path(r"e:\vscode\claudecode\.claude\skills\visualize\visualizations")
```
- **Issue:**
  - Won't work on other machines
  - Hardcoded date makes script brittle
  - No ability to pass different data sources
  - Violates portability and reusability
- **Fix:** Make paths configurable as function arguments (see refactored example above)

#### 3. **No Error Handling**
- **Lines 24-30:** No try-except blocks for file I/O
- **Issue:** Script crashes silently if files missing; no recovery mechanism
- **Recommendation:**
```python
def load_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load all CSV files from data directory."""
    required_files = [
        "dim_customer.csv",
        "dim_date.csv",
        "dim_product.csv",
        "dim_store.csv",
        "fact_sales.csv",
        "fact_returns.csv",
    ]

    data = {}
    for filename in required_files:
        filepath = data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Required file missing: {filepath}")
        try:
            data[filename.replace(".csv", "")] = pd.read_csv(filepath)
        except pd.errors.ParserError as e:
            raise ValueError(f"Failed to parse {filename}: {e}")
```

#### 4. **No Type Hints (High Priority)**
- **Lines 1-177:** Zero type hints in entire script
- **Issue:** Violates project standards (CLAUDE.md requirement)
- **Impact:** Makes code harder to understand and maintain
- **Recommendation:** Add type hints to all variables and functions (see refactored example)

#### 5. **No Docstrings (High Priority)**
- **Issue:** Script has only module-level docstring; no function docstrings
- **Violation:** PEP 257 requires docstrings for all public functions
- **Fix:** Add comprehensive docstrings to each function

#### 6. **Hardcoded Data Transformation Logic (Medium)**
- **Lines 36-47:** Merge operations are repeated twice for sales and returns
- **Issue:** Code duplication; difficult to maintain
- **Recommendation:**
```python
def merge_data(fact_df: pd.DataFrame, dimension_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Generic merge function for fact and dimension tables."""
    result = fact_df.copy()
    dimension_mappings = {
        "date_sk": "dim_date",
        "store_sk": "dim_store",
        "product_sk": "dim_product",
        "customer_sk": "dim_customer",
    }

    for foreign_key, dim_table in dimension_mappings.items():
        if foreign_key in result.columns and dim_table in dimension_dfs:
            result = result.merge(
                dimension_dfs[dim_table],
                left_on=foreign_key,
                right_on=foreign_key,
                how="left"
            )
    return result

# Usage:
sales_data = merge_data(data["fact_sales"], data)
returns_data = merge_data(data["fact_returns"], data)
```

#### 7. **Inconsistent Plotting Code (Medium)**
- **Lines 65-174:** 8 nearly identical visualization blocks with repeated code
- **Issue:** ~110 lines of repetitive code; any bug must be fixed 8 times
- **Recommendation:**
```python
def create_visualization(
    data: pd.DataFrame,
    group_by: str,
    value_col: str,
    title: str,
    output_path: Path,
    plot_type: str = "bar",
    top_n: int = None,
    figsize: tuple = (12, 6),
    color: str = "#1f77b4",
) -> None:
    """Generic visualization function."""
    grouped_data = data.groupby(group_by)[value_col].sum().sort_values(ascending=False)

    if top_n:
        grouped_data = grouped_data.head(top_n)

    plt.figure(figsize=figsize)
    if plot_type == "bar":
        grouped_data.plot(kind="bar", color=color)
    elif plot_type == "barh":
        grouped_data.plot(kind="barh", color=color)
    elif plot_type == "line":
        plt.plot(grouped_data.index, grouped_data.values, linewidth=2, color=color)

    plt.title(title, fontsize=14, fontweight="bold")
    plt.xlabel(value_col)
    plt.ylabel(group_by)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

# Usage:
create_visualization(
    sales_data,
    group_by="store_name",
    value_col="net_amount",
    title="Total Sales by Store",
    output_path=output_dir / "sales_by_store.png",
    plot_type="bar",
    color="#2ca02c"
)
```

#### 8. **Unused Import & Magic Values (Medium)**
- **Line 11:** `datetime` imported but never used
- **Lines 19-21:** Magic numbers/strings for matplotlib config with no documentation
- **Recommendation:**
```python
from datetime import datetime  # Remove if unused

# Document config
PLOT_CONFIG = {
    "style": "whitegrid",
    "figsize": (12, 6),
    "font_size": 10,
    "dpi": 300,
    "color_palette": {
        "sales": "#1f77b4",
        "returns": "#d62728",
        "stores": "#2ca02c",
    }
}

sns.set_style(PLOT_CONFIG["style"])
plt.rcParams['figure.figsize'] = PLOT_CONFIG["figsize"]
plt.rcParams['font.size'] = PLOT_CONFIG["font_size"]
```

#### 9. **Potential Data Quality Issues (Medium)**
- **Lines 67, 122-123:** No handling of missing dates or NaN values
- **Issue:** Visualizations may be misleading if data has nulls
- **Recommendation:**
```python
def plot_sales_trend(sales_data: pd.DataFrame, output_dir: Path) -> None:
    """Create sales trend visualization."""
    sales_by_date = sales_data.groupby("date")["net_amount"].sum().reset_index()

    # Validate data
    if sales_by_date["date"].isnull().any():
        logger.warning("Found null dates; removing for trend visualization")
        sales_by_date = sales_by_date.dropna(subset=["date"])

    sales_by_date = sales_by_date.sort_values("date")

    if sales_by_date.empty:
        logger.error("No valid data for sales trend visualization")
        return

    # ... rest of plotting
```

#### 10. **Missing Configuration File**
- **Issue:** All hardcoded values make the script inflexible
- **Recommendation:** Create a `config.yaml` or `.env` file:
```yaml
# visualize_config.yaml
data_dir: .claude/skills/fetchAPI/data/latest
output_dir: .claude/skills/visualize/visualizations
plot_config:
  dpi: 300
  figsize: [12, 6]
  font_size: 10
visualizations:
  - name: sales_trend_over_time
    type: line
    group_by: date
    value_col: net_amount
```

#### 11. **Inconsistent Customer Name Handling (Low)**
- **Line 164:** `returns_data['customer_name'] = returns_data['last_name']`
- **Issue:** Column naming inconsistency; why rename when `last_name` exists?
- **Recommendation:**
```python
# Use consistent column name throughout
returns_by_customer = returns_data.groupby("last_name")["refund_amount"].sum()
# Or create standardized customer identifier earlier
```

---

### Code Quality Score

| Criterion | Score | Notes |
|-----------|-------|-------|
| Structure | 2/10 | No functions; entirely procedural |
| PEP 8 Compliance | 3/10 | No docstrings; no type hints; hardcoded values |
| Type Hints | 0/10 | None present (required by project standards) |
| Documentation | 2/10 | Only module-level docstring |
| Error Handling | 1/10 | No try-except blocks |
| Maintainability | 1/10 | Extreme code duplication; hardcoded paths |
| Performance | 6/10 | Acceptable but could be optimized with batched plotting |
| **Overall** | **2/10** | **Requires major refactoring** |

---

---

## Summary of Recommendations by Priority

### Critical Issues (Must Fix)
1. **convert_to_parquet.py**: Rename file (typo in filename)
2. **convert_to_parquet.py**: Remove hardcoded paths; make configurable
3. **visualize_data.py**: Refactor into functions with proper structure
4. **visualize_data.py**: Remove hardcoded absolute paths
5. **visualize_data.py**: Add type hints and docstrings (project standard)

### High Priority (Should Fix)
1. **convert_to_parquet.py**: Improve exception handling (too generic)
2. **convert_to_parquet.py**: Replace `print()` with logging module
3. **visualize_data.py**: Add error handling for file I/O
4. **visualize_data.py**: Remove code duplication in plotting functions
5. **visualize_data.py**: Create reusable generic visualization function

### Medium Priority (Nice to Have)
1. **convert_to_parquet.py**: Add data validation for CSV files
2. **convert_to_parquet.py**: Create configuration management system
3. **visualize_data.py**: Add data quality checks
4. **visualize_data.py**: Create configuration file for flexibility
5. **Both**: Add requirements.txt or update pyproject.toml with dependencies

### Low Priority
1. **visualize_data.py**: Remove unused imports
2. **visualize_data.py**: Standardize column naming conventions
3. **convert_to_parquet.py**: Optimize file size calculation

---

## Alignment with Project Standards (CLAUDE.md)

### Violations in `visualize_data.py`
- ✗ **Type Annotations**: Required but absent (0/0 functions have type hints)
- ✗ **Docstrings**: Required but minimal (only module-level, no function docstrings)
- ✗ **Code Organization**: Not organized into functions; purely procedural
- ✗ **Error Handling**: Missing try-except blocks entirely
- ✓ PEP 8: Generally follows style (indentation, spacing)

### Violations in `convert_to_parquet.py`
- ✓ **Type Annotations**: Present (good)
- ✓ **Docstrings**: Present for all functions (good)
- ✗ **Code Organization**: Decent but hardcoded values reduce reusability
- ✓ **Error Handling**: Basic but could be improved
- ✗ **Hardcoded Paths**: Reduces portability
- ✓ PEP 8: Generally follows style

---

## Testing Recommendations

### For `convert_to_parquet.py`
```python
# tests/test_convert_to_parquet.py
import pytest
from pathlib import Path
import pandas as pd
from convert_to_parquet import get_latest_folder, convert_csv_to_parquet

def test_get_latest_folder_with_valid_path(tmp_path):
    """Test getting latest folder from directory."""
    # Create test folders
    (tmp_path / "2026-01-01").mkdir()
    (tmp_path / "2026-03-22").mkdir()

    name, path = get_latest_folder(str(tmp_path))
    assert name == "2026-03-22"

def test_get_latest_folder_missing_path():
    """Test error handling for missing path."""
    with pytest.raises(FileNotFoundError):
        get_latest_folder("/nonexistent/path")

def test_convert_csv_with_empty_file(tmp_path):
    """Test conversion of empty CSV."""
    # Create empty CSV
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")

    # Should handle gracefully or raise appropriate error
```

### For `visualize_data.py`
```python
# tests/test_visualize_data.py
def test_load_data_with_valid_directory(tmp_path):
    """Test loading data from valid directory."""
    # Create mock CSV files
    # Assert data loaded correctly

def test_calculate_kpis(sample_data):
    """Test KPI calculations."""
    kpis = calculate_kpis(sample_data["fact_sales"], sample_data["fact_returns"])
    assert kpis["total_sales"] > 0
    assert kpis["net_sales"] == kpis["total_sales"] - kpis["total_returns"]

def test_visualization_with_missing_columns(tmp_path):
    """Test visualization doesn't crash with missing columns."""
    # Should handle gracefully or raise informative error
```

---

## Files Modified

This review covers:
- `.claude/skills/migrate/scripts/covert_to_parquet.py`
- `.claude/skills/visualize/scripts/visualize_data.py`

---

## Next Steps

1. **For `covert_to_parquet.py`:**
   - Rename file to `convert_to_parquet.py`
   - Refactor paths into configuration
   - Improve exception handling
   - Add logging module

2. **For `visualize_data.py`:**
   - Refactor entire script into functions
   - Add type hints to all functions
   - Add comprehensive docstrings
   - Remove hardcoded paths
   - Add error handling
   - Extract plotting into generic function

3. **For Both:**
   - Update `pyproject.toml` with dependencies
   - Create unit tests
   - Add configuration files
   - Document expected data formats

---

**End of Review**
