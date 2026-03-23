---
name: Common Code Quality Patterns Observed
description: Recurring issues, anti-patterns, and structural problems found in Python scripts reviewed
type: feedback
---

## Recurring Anti-Patterns Identified

### 1. Hardcoded Absolute Paths
**Pattern:** Scripts contain absolute Windows-style paths embedded in code
```python
DATA_DIR = Path(r"e:\vscode\claudecode\.claude\skills\fetchAPI\data\2026-03-22_00-45-35")
source_base = r".\.claude\skills\fetchAPI\data"
```

**Why:** Makes scripts non-portable, breaks on different machines/environments, difficult to test, brittle to directory structure changes

**How to apply:** Always make paths configurable via function parameters or configuration files; use relative paths with `Path(__file__).parent` for relative locations; accept paths as CLI arguments or environment variables

---

### 2. Procedural Code with No Functions
**Pattern:** Entire script is sequential operations at module level with no abstraction
```python
# Lines 1-177 with no functions, just procedural steps
data = pd.read_csv(...)
# ... more processing ...
plt.plot(...)
plt.savefig(...)
```

**Why:** Cannot be reused, tested, debugged, or repurposed; violates PEP 8 and project standards; changes require understanding entire script flow

**How to apply:** Always organize code into functions with single responsibility; extract data loading, transformations, and visualizations into separate functions; make functions take parameters and return values

---

### 3. Using `print()` Instead of Logging
**Pattern:** Informational output via `print()` statements
```python
print(f"Found {len(csv_files)} CSV file(s)")
print(f"  [ERR] Error converting {csv_file.name}: {str(e)}")
```

**Why:** No control over verbosity levels, cannot be captured to files, no timestamps, conflates user output with diagnostic info

**How to apply:** Use `logging` module for all non-interactive output; configure level (DEBUG, INFO, WARNING, ERROR); reserve `print()` only for interactive CLI prompts or final user-facing results

---

### 4. Generic Exception Handling
**Pattern:** Catching broad `Exception` without distinguishing error types
```python
try:
    df = pd.read_csv(csv_file)
    df.to_parquet(parquet_path, engine="pyarrow", index=False)
except Exception as e:
    print(f"  [ERR] Error: {str(e)}")
```

**Why:** Catches programming errors inadvertently; difficult to debug; doesn't distinguish recoverable vs. fatal errors; masks bugs

**How to apply:** Catch specific exception types (FileNotFoundError, pd.errors.ParserError, IOError); handle each differently; only catch exceptions you can actually recover from; re-raise or propagate unexpected errors

---

### 5. Missing Type Hints
**Pattern:** Functions and variables without type annotations
```python
def load_data(data_dir):  # No type hints
    data = pd.read_csv(...)  # No type hint for return
```

**Why:** Violates project standards (CLAUDE.md requires type hints); harder to understand code intent; makes IDE autocomplete less useful; harder to catch bugs early

**How to apply:** Add type hints to all function parameters and return types; use `from typing import Dict, Optional, List` for complex types; use `Path | str` for union types (Python 3.10+)

---

### 6. Missing or Inadequate Documentation
**Pattern:** No docstrings for functions or inconsistent documentation
```python
def convert_csv_to_parquet(source_folder, output_base_path, folder_name):
    # No docstring, unclear what parameters do
```

**Why:** Violates PEP 257; makes code harder to understand; no IDE tooltips; unclear intent; reduces maintainability

**How to apply:** Add docstrings to all functions with Args, Returns, Raises sections; document non-obvious logic; use consistent format (Google style or NumPy style)

---

### 7. Code Duplication
**Pattern:** Nearly identical code blocks repeated multiple times
```python
# Lines 65-78: Sales trend plot
plt.figure(figsize=(14, 6))
plt.plot(sales_by_date["date"], sales_by_date["net_amount"], ...)
plt.savefig(OUTPUT_DIR / "sales_trend_over_time.png", ...)

# Lines 125-133: Returns trend plot (near-identical)
plt.figure(figsize=(14, 6))
plt.plot(returns_by_date["date"], returns_by_date["refund_amount"], ...)
plt.savefig(OUTPUT_DIR / "returns_trend_over_time.png", ...)
```

**Why:** Bugs must be fixed multiple times; changes ripple across codebase; violates DRY principle; increases maintenance burden

**How to apply:** Extract common logic into reusable functions with parameters; use loops for repetitive operations; parameterize differences

---

### 8. No Error Handling for File I/O
**Pattern:** File operations without try-except
```python
dim_customer = pd.read_csv(DATA_DIR / "dim_customer.csv")
dim_date = pd.read_csv(DATA_DIR / "dim_date.csv")
# If any file missing, script crashes silently
```

**Why:** Script fails with unclear error messages; no graceful degradation; hard to debug missing data issues

**How to apply:** Wrap file I/O in try-except; distinguish FileNotFoundError from ParserError; log or raise with informative messages; validate expected files exist before processing

---

### 9. Hardcoded Configuration Values
**Pattern:** Settings embedded directly in code
```python
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['dpi'] = 300
```

**Why:** Cannot change behavior without code changes; difficult to use in different environments (test vs. prod); violates 12-factor app principles

**How to apply:** Extract to configuration file (YAML, JSON, .env); create Config class or dict; pass as function arguments; use environment variables for sensitive/environment-specific values

---

### 10. No Data Validation
**Pattern:** Assumes data is always valid without checking
```python
df = pd.read_csv(csv_file)
df.to_parquet(parquet_path)  # Never checks if df is empty, has nulls, etc.
```

**Why:** Produces incorrect outputs silently; hard to debug; may corrupt downstream analysis

**How to apply:** Validate data after loading (check shape, columns, dtypes, nulls); log warnings for data quality issues; skip or handle problematic records; fail fast with clear error messages

---

## Project-Specific Conventions to Enforce

### Based on CLAUDE.md Requirements

1. **Type Annotations Required** - All functions must have type hints
2. **Docstrings Required** - PEP 257 format for all public functions
3. **PEP 8 Compliance** - Follow Python style guide strictly
4. **Meaningful Names** - Use `camelCase` for functions (as per project standard, though standard Python is `snake_case`)
5. **Clear Organization** - Separate concerns into modules/functions

---

## Recommendation for Future Reviews

When reviewing Python scripts, prioritize checking for:

1. **Structure**: Are there functions? Is code modularized?
2. **Type Hints**: Do all functions have parameter and return type annotations?
3. **Docstrings**: Are all functions documented (Args, Returns, Raises)?
4. **Paths**: Are hardcoded paths present? Can they be made configurable?
5. **Error Handling**: Are exceptions caught? Are they specific or generic?
6. **Logging**: Are `print()` statements used inappropriately?
7. **Duplication**: Is there repeated code that could be extracted?
8. **Configuration**: Are magic values hardcoded?
9. **Testing**: Are functions testable? Can they be unit tested?
10. **Standards**: Does code follow CLAUDE.md requirements?

These checks catch 90% of issues in Python scripts reviewed so far.
