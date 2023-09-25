from datetime import datetime
from typing import List, Tuple
import ssl

import google_play_scraper as gps
from google_play_scraper.features.reviews import MAX_COUNT_EACH_FETCH

from google_play_scraper.features.reviews import _ContinuationToken
from review_etl.etl.scraper.scraper import BaseScraper


ssl._create_default_https_context = ssl._create_unverified_context
# THIS SCRAPER IS BUGGY. COUNTRY FLAG HAS NO ROLE
# JUST USE LANG PARAM TO SCRAPE REVIEW PER DIFF LANGUAGE
# REVIEWS FROM US ARE SAME AS REVIEWS FROM GERMANY IF SAME LANGUAGE IS SPECIFIED
COUNTRY = "us"


class PlayStoreScraper(BaseScraper):
    """Google's Play Store Scraper"""

    source: str = "play_store"

    def __init__(self):
        super().__init__()

    def get_company_info(self, id) -> dict:
        response = gps.app(id, lang="en", country=COUNTRY)
        return {
            "_id": {"company_id": id, "source": PlayStoreScraper.source},
            "company_id": id,
            "name": response["title"],
            "num_installs": response.get("installs"),
            "rating": response.get("score"),
            "num_ratings": response.get("score"),
            "num_reviews": response.get("reviews"),
            "genre": response.get("genre"),
            "source": self.source,
        }

    def _parse_review_response(
        self, response: dict, company_id: str, lang: str
    ) -> dict:
        return {
            "_id": response["reviewId"],
            "review": response.get("content"),
            "rating": response.get("score"),
            "helpful_count": response.get("thumbsUpCount"),
            "date": response["at"],
            "company_id": company_id,
            "lang": lang,
        }

    def _scrape_once(
        self, company_id, lang, continuation_token: _ContinuationToken = None
    ) -> Tuple[dict, _ContinuationToken]:
        # TODO add documentation
        reviews, token = gps.reviews(
            company_id, lang, country=COUNTRY, continuation_token=continuation_token
        )
        reviews_parsed = [
            self._parse_review_response(response, company_id, lang)
            for response in reviews
        ]
        return reviews_parsed, token

    def scrape_until(
        self, company_id: str, lang: str, date: datetime = None
    ) -> List[dict]:
        # NOTE ABOUT THE BUGGY API ABOVE!
        """This method returns all the reviews for a specific
        company--anguage combination up until the review.
        Args:
            company_id (str): id of the company at source
            lang (str): language of reviews
            date (datetime, optional): the time until when the reviews are scraped

        Returns:
            dict: Keys of which determine the rows of the company id table
        """
        if date is None:
            # scrape all reviews as no min date
            reviews = gps.reviews_all(
                company_id, sleep_milliseconds=10, country=COUNTRY, lang=lang
            )
            return [
                self._parse_review_response(review, company_id, lang)
                for review in reviews
            ]
        # scrape until the date is reached!
        all_reviews = []
        token = None
        while True:
            reviews, token = self._scrape_once(company_id, lang, token)
            reviews_valid = [review for review in reviews if review["date"] > date]
            # stop if date condition is not satisfied
            if len(reviews_valid) == 0:
                break
            all_reviews.extend(reviews_valid)
            # stop loop as we don't have token anymore
            if token.token is None:
                break
        return all_reviews
