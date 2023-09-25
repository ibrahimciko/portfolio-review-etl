from review_etl.etl.scraper.scraper import BaseScraper


class AppStore(BaseScraper):
    source: str = "app_store"

    def __init__(self):
        super().__init__()

    def get_company_info(self, id, country) -> dict:
        # NOT IMPLEMENTED YET
        raise NotImplementedError
