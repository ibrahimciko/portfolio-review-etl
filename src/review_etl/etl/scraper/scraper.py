from abc import abstractmethod
from datetime import datetime
from typing import List


# BU SIKKO SCRAPER'I farkli Scraperlar icin bir interface teskil etsin diye koymustum ama
# ama concrete scraperlar o kadar kotu ki ki common methodlarla yazmak cok zor
# Bazilarinda sadece guncelden eskiye review scrape edebiliyorsun vesaire
class BaseScraper:
    """This is the interface we are using for Scrapers. When we want to implement a new Scraper for a new source
    such as AppStore, the app store scraper needs to implement the abstract methods below.
    """

    @abstractmethod
    def get_company_info(self, id: str) -> dict:
        """This method returns all the meta information related to an app in a source.
        There is no way to query the source with keywords. That is why one needs to make sure that the app exists
        with correct id

        Args:
            id (str):

        Returns:
            dict: Keys of which determine the rows of the company id table
        """

    @abstractmethod
    def scrape_until(
        self, company_id: str, lang: str, date: datetime = None
    ) -> List[dict]:
        """This method returns all the reviews for a specific
        company-language combination up until the review.
        Args:
            company_id (str): id of the company at source
            lang (str): language of reviews
            date (datetime): the time until when the reviews are scraped

        Returns:
            List[dict]: Keys of which determine the rows of the company id table
        """
