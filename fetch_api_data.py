"""
API Data Fetcher using async httpx.

Fetches CSV files from specified URLs and saves them to a timestamped directory
with comprehensive logging.
"""

import asyncio
import httpx
import logging
import os
from datetime import datetime
from pathlib import Path


# URLs to fetch data from
API_URLS = [
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
]


def setupLogger(logDir: str) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        logDir: Directory where log file will be saved.

    Returns:
        Configured logger instance.
    """
    Path(logDir).mkdir(parents=True, exist_ok=True)
    logFile = os.path.join(logDir, "fetchAPI.log")

    logger = logging.getLogger("fetchAPI")
    logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(logFile)
    fileHandler.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


async def fetchData(client: httpx.AsyncClient, url: str) -> tuple[str, str | None]:
    """
    Fetch data from a single URL.

    Args:
        client: httpx AsyncClient instance.
        url: URL to fetch data from.

    Returns:
        Tuple of (filename, content) or (filename, None) if failed.
    """
    filename = url.split("/")[-1]
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return filename, response.text
    except httpx.HTTPError as e:
        return filename, None


async def fetchAllData(urls: list, logger: logging.Logger) -> dict:
    """
    Fetch data from all URLs concurrently.

    Args:
        urls: List of URLs to fetch.
        logger: Logger instance for logging.

    Returns:
        Dictionary mapping filenames to content.
    """
    logger.info(f"Starting to fetch data from {len(urls)} URLs")

    async with httpx.AsyncClient() as client:
        tasks = [fetchData(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

    fetchedData = {}
    for filename, content in results:
        if content:
            fetchedData[filename] = content
            logger.info(f"Successfully fetched: {filename}")
        else:
            logger.error(f"Failed to fetch: {filename}")

    logger.info(
        f"Fetch complete: {len(fetchedData)}/{len(urls)} URLs successful"
    )
    return fetchedData


def saveData(fetchedData: dict, dataDir: str, logger: logging.Logger) -> None:
    """
    Save fetched data to CSV files.

    Args:
        fetchedData: Dictionary of filenames and content.
        dataDir: Directory to save files.
        logger: Logger instance for logging.
    """
    Path(dataDir).mkdir(parents=True, exist_ok=True)

    for filename, content in fetchedData.items():
        filepath = os.path.join(dataDir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Saved: {filename} to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save {filename}: {e}")


async def main() -> None:
    """
    Main function to orchestrate API fetching and data saving.
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Set up directories
    dataDir = os.path.join(".claude/skills/fetchAPI/data", timestamp)
    logDir = os.path.join(".claude/skills/fetchAPI/logs", timestamp)

    # Set up logger
    logger = setupLogger(logDir)
    logger.info("=" * 50)
    logger.info("fetchAPI: Starting API data fetch process")
    logger.info("=" * 50)

    # Fetch data
    fetchedData = await fetchAllData(API_URLS, logger)

    # Save data
    if fetchedData:
        saveData(fetchedData, dataDir, logger)
        logger.info(f"Data saved to: {dataDir}")
    else:
        logger.warning("No data was fetched successfully")

    logger.info("=" * 50)
    logger.info("fetchAPI: Process complete")
    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
