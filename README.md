# Claude Code

A Python project demonstrating data integration, LLM interaction, and data pipeline orchestration using Claude AI, Apache Airflow, and modern Python practices.

## Overview

Claude Code is a comprehensive project that combines:
- **LLM Integration** - Leveraging Claude AI through LangChain for intelligent data processing
- **Async API Data Fetching** - Concurrent data retrieval from external sources
- **Data Processing** - Pandas-based data manipulation and transformation
- **Pipeline Orchestration** - Apache Airflow DAGs for workflow automation and asset-based scheduling
- **Jupyter Notebooks** - Interactive exploration and experimentation environment

## Features

✨ **Key Features:**
- Async API data fetching with comprehensive logging
- LLM-powered code generation and data insights
- Pandas DataFrame creation and manipulation
- Apache Airflow asset-based DAG scheduling
- Type-annotated Python code following PEP 8
- Comprehensive documentation and examples
- Environment variable management with `.env` support

## Project Structure

```
claudecode/
├── main.py                      # Main entry point
├── fetch_api_data.py            # Async API data fetcher
├── create_dataframe.py          # DataFrame creation utilities
├── 1_llm_call.ipynb             # LLM integration example notebook
├── Airflow_Project/             # Apache Airflow data pipelines
│   ├── dags/
│   │   ├── data_fetch.py        # Producer DAG - fetches and transforms data
│   │   └── data_report.py       # Consumer DAG - generates reports
│   └── README.md                # Airflow documentation
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Alternative dependency specification
├── .env                         # Environment variables (not in git)
├── .python-version              # Python version specification
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.14 or higher
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd claudecode
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   # Or using the project tool if installed
   uv sync
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env  # Create from template if available
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## Dependencies

Core dependencies (from `pyproject.toml`):
- **langchain-anthropic** ≥ 1.4.0 - Claude AI integration
- **httpx** ≥ 0.24.0 - Async HTTP client for API calls
- **pandas** ≥ 3.0.1 - Data manipulation and analysis
- **pyarrow** ≥ 23.0.1 - Parquet and Arrow data format support
- **python-dotenv** ≥ 0.9.9 - Environment variable management

## Usage

### Running the Main Script

```bash
python main.py
```

### Fetching API Data

The `fetch_api_data.py` script fetches CSV files from specified URLs and saves them with timestamped logging:

```bash
python fetch_api_data.py
```

**Output:**
- Data files: `.claude/skills/fetchAPI/data/<timestamp>/`
- Logs: `.claude/skills/fetchAPI/logs/<timestamp>/fetchAPI.log`

### Creating Sample DataFrames

```bash
python create_dataframe.py
```

Outputs a sample DataFrame with 3 columns and 5 rows of demonstration data.

### Using Jupyter Notebooks

Launch Jupyter to explore the LLM integration example:

```bash
jupyter notebook 1_llm_call.ipynb
```

The notebook demonstrates:
- Claude AI API integration via LangChain
- Prompt engineering for code generation
- Environment variable validation

### Apache Airflow Pipelines

For detailed information about the Airflow DAGs, see [Airflow_Project/README.md](Airflow_Project/README.md).

**Quick Start:**
```bash
# Start Airflow webserver
airflow webserver --port 8080

# Start scheduler
airflow scheduler

# Trigger data_fetch DAG
airflow dags trigger data_fetch
```

The project includes:
- **data_fetch DAG** - Fetches external data, transforms it, and creates an asset
- **data_report DAG** - Consumes the asset from data_fetch and generates reports

## Development Guidelines

This project follows PEP 8 and the standards outlined in [CLAUDE.md](.claude/CLAUDE.md):

### Code Standards
- **Type Annotations** - All functions use type hints
- **Docstrings** - PEP 257 compliant docstrings for public APIs
- **Naming Conventions** - `camelCase` for functions/methods, `snake_case` for variables
- **Error Handling** - Thoughtful exception handling with proper logging

### Examples

**Function with Type Hints:**
```python
async def fetchData(client: httpx.AsyncClient, url: str) -> tuple[str, str | None]:
    """
    Fetch data from a single URL.

    Args:
        client: httpx AsyncClient instance.
        url: URL to fetch data from.

    Returns:
        Tuple of (filename, content) or (filename, None) if failed.
    """
    # Implementation...
```

## Key Components

### fetch_api_data.py
Async API data fetcher that:
- Fetches CSV files from GitHub repositories concurrently
- Implements comprehensive logging to file and console
- Saves data to timestamped directories
- Includes error handling and success reporting

### create_dataframe.py
DataFrame utilities for creating sample data structures with:
- Consistent data types and structures
- Documentation and examples
- Reusable functions for testing and development

### 1_llm_call.ipynb
Interactive notebook demonstrating:
- Claude AI integration through LangChain
- API key validation
- Prompt engineering examples
- Code generation capabilities

### Airflow DAGs
Asset-based workflow orchestration featuring:
- Producer DAG with data transformation pipeline
- Consumer DAG with automatic triggering
- JSON data processing and storage
- Natural dependency management through assets

## Environment Variables

The project requires the following environment variable:

- **ANTHROPIC_API_KEY** - Your Claude API key from Anthropic

Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your-api-key-here
```

## Logging

The project implements structured logging:
- Console output at INFO level
- File logging at DEBUG level
- Timestamped log directories
- Detailed error tracking

Logs are stored in: `.claude/skills/fetchAPI/logs/<timestamp>/`

## Project Features

### Async Operations
- Non-blocking API calls using `httpx.AsyncClient`
- Concurrent fetching of multiple URLs with `asyncio.gather()`
- Efficient resource utilization

### Data Processing
- Pandas DataFrames for data manipulation
- Arrow integration for efficient data formats
- CSV file handling

### LLM Integration
- Claude AI model through LangChain
- Support for code generation and analysis
- Environment-based API key management

### Pipeline Orchestration
- Apache Airflow for workflow management
- Asset-based scheduling for DAG dependencies
- Task-based architecture with Python decorators

## Contributing

Follow these guidelines when contributing:
1. Adhere to PEP 8 and project coding standards
2. Add type hints and docstrings to all functions
3. Test your changes thoroughly
4. Commit often with meaningful messages
5. Review code before submitting pull requests

For more details, see [CLAUDE.md](.claude/CLAUDE.md).

## Useful Resources

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [LangChain Documentation](https://docs.langchain.com/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [HTTPX Documentation](https://www.python-httpx.org/)

## License

[Add your license information here]

## Contact

For questions or suggestions, contact the project maintainer.

---

*Last Updated: 2026-03-24*
