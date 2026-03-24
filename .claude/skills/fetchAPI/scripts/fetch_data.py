"""
Fetch data from multiple CSV URLs using async httpx.
"""

import asyncio
import httpx
import csv
from pathlib import Path
from datetime import datetime
import logging
import sys

# URLs to fetch
URLS = [
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
]

BASE_DIR = Path(".claude/skills/fetchAPI")
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"


def setup_logging(timestamp_str: str):
    """Set up logging configuration."""
    log_dir = LOGS_DIR / timestamp_str
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "fetchAPI.log"

    logger = logging.getLogger("fetchAPI")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    logger.handlers.clear()

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger, log_file


async def fetch_csv(client: httpx.AsyncClient, url: str, output_path: Path, logger: logging.Logger) -> bool:
    """Fetch a CSV file from URL and save it."""
    filename = url.split("/")[-1]

    try:
        logger.info(f"Fetching: {url}")
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()

        # Save the file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="") as f:
            f.write(response.text)

        logger.info(f"[OK] Successfully saved: {filename} ({len(response.text)} bytes)")
        return True

    except httpx.HTTPError as e:
        logger.error(f"[ERROR] HTTP Error fetching {filename}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"[ERROR] Error saving {filename}: {str(e)}")
        return False


async def main():
    """Main function to fetch all data."""
    # Create timestamp
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Setup logging
    logger, log_file = setup_logging(timestamp_str)

    logger.info("=" * 60)
    logger.info("Starting API Data Fetch")
    logger.info("=" * 60)
    logger.info(f"Timestamp: {timestamp_str}")
    logger.info(f"Number of URLs to fetch: {len(URLS)}")

    # Create data directory
    data_dir = DATA_DIR / timestamp_str
    data_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    results = {}

    async with httpx.AsyncClient() as client:
        tasks = []
        for url in URLS:
            filename = url.split("/")[-1]
            output_path = data_dir / filename
            task = fetch_csv(client, url, output_path, logger)
            tasks.append((filename, task))

        # Execute all tasks
        for filename, task in tasks:
            result = await task
            results[filename] = result

    # Summary
    logger.info("=" * 60)
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful

    logger.info(f"Results Summary:")
    logger.info(f"  Total URLs: {len(results)}")
    logger.info(f"  Successful: {successful}")
    logger.info(f"  Failed: {failed}")

    for filename, success in results.items():
        status = "[OK] SUCCESS" if success else "[FAILED]"
        logger.info(f"  {status}: {filename}")

    logger.info("=" * 60)
    logger.info("API Data Fetch Completed")
    logger.info("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
