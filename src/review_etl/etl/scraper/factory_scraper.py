import logging

from review_etl.etl.scraper.scraper import BaseScraper
from review_etl.etl.scraper.play_store import PlayStoreScraper
from review_etl.etl.scraper.app_store import AppStore


logger = logging.getLogger("info")


def get_scraper_by_source(source: str) -> BaseScraper:
    """Factory method to initialize the scraper given the source.

    Args:
        source (str): Source of reviews; e.g., app_store or play_store

    Returns:
        BaseScraper: Implementation of one of the child scrapers.
    """
    options = {PlayStoreScraper.source: PlayStoreScraper, AppStore.source: AppStore}
    if source in options:
        logger.info(f"Scraper with source {source} chosen.")
        return options[source]()
    logger.error(f"Not a valid scraper with name: {source}. Choose among {options}")
