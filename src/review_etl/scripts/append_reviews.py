import os
import logging
import traceback
import sys
from datetime import datetime
from typing import List
from typing import Optional
import itertools


from dotenv import load_dotenv
from dotenv import find_dotenv
from pymongo import DESCENDING
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from pymongo.errors import BulkWriteError

from review_etl.common.mongo_db import get_connect_string
from review_etl.etl.scraper.factory_scraper import get_scraper_by_source
from review_etl.etl.scraper.scraper import BaseScraper
from review_etl.config.mongo_constants import DB_NAME
from review_etl.config.mongo_constants import REVIEW_COLLECTION
from review_etl.config.mongo_constants import COMPANY_COLLECTION
from review_etl.common.logger_utils import setup_logger
from review_etl.scripts.append_company import main as append_company_main
from review_etl.common.argparse_utils import parse_arguments


logger = logging.getLogger(setup_logger("append_review", "./logs"))


def get_latest_review_date(
    collection: Collection, company_id: str, lang: str
) -> Optional[datetime]:
    # TODO add documentation
    res = list(
        collection.find({"company_id": company_id, "lang": lang}, {"date": 1})
        .sort("date", DESCENDING)
        .limit(1)
    )
    # empty query
    if len(res) == 0:
        latest_date = None
    else:
        latest_date = res[0]["date"]
    return latest_date


def insert_reviews(
    collection: Collection, reviews: List[dict], unsafe_insertion: bool = False
):
    """Insert reviews

    Args:
        collection (Collection): Name of the collection where reviews are stored
        reviews (list): List of scraped reviews
        unsafe_insertion: If False, queries all documents and only insert reviews that have different _id value.
            If True, due to some bug in the scraper, we can get duplicate key error.
    """
    num_reviews = len(reviews)
    if num_reviews == 0:
        logger.info(f"No new reviews found. Nothing will be written to db.")
        return

    if unsafe_insertion:
        new_reviews = reviews.copy()

    else:
        # query database for review id's
        existing_ids = {el["_id"] for el in collection.find({}, {"_id": 1})}
        new_reviews = [r for r in reviews if r["_id"] not in existing_ids]
        num_reviews = len(new_reviews)

    logger.info(f"{num_reviews} new reviews found and will be appended to db.")
    _ = collection.insert_many(new_reviews)
    # TODO verify inserted ids before saying successful!
    logger.info(f"Successful")


def main(
    source: str,
    company_ids: List[str] = None,
    lang: List[str] = None,
    unsafe_insertion: bool = False,
    company_ids_from_db: bool = False,
):
    load_dotenv(find_dotenv())
    with MongoClient(
        get_connect_string(os.environ.get("MONGODB_USR"), os.environ.get("MONGODB_PWD"))
    ) as client:
        db = client[DB_NAME]
        if company_ids_from_db:
            # get company ids from already existing ones!
            companies = [
                doc["company_id"]
                for doc in db[COMPANY_COLLECTION].find({}, {"company_id": 1})
            ]
        else:
            # use the passed argument as company_id
            if company_ids is None:
                logger.info(
                    f"Please provide a valid company_id: {company_ids}. Aborting ..."
                )
                sys.exit("Invalid company name")
            else:
                # upsert company info to company collection
                append_company_main(source, company_ids)
                companies = company_ids.copy()
        # init scraper
        scraper = get_scraper_by_source(source)
        # get review collection
        review_col = db[REVIEW_COLLECTION]
        for company, language in list(itertools.product(companies, lang)):
            logger.info(f"Scraping for company: {company}, language: {language}")
            try:
                latest_date = get_latest_review_date(review_col, company, language)
                logger.info(f"Latest review date in the database: {latest_date}")
                reviews = scraper.scrape_until(company, language, latest_date)
                insert_reviews(review_col, reviews, unsafe_insertion)
            except (DuplicateKeyError, BulkWriteError) as error:
                logger.error(
                    f"Failed to write as the review exists!\n{traceback.format_exc()}"
                )
            except Exception:
                logger.error(f"Unknown Error\n{traceback.format_exc()}")


if __name__ == "__main__":
    args = parse_arguments()
    main(
        args["source"],
        args["company_ids"],
        args["lang"],
        args["unsafe_insertion"],
        args["company_ids_from_db"],
    )
