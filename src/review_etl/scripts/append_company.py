import os
import logging
import traceback
from typing import List

from dotenv import load_dotenv
from dotenv import find_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from review_etl.common.mongo_db import get_connect_string
from review_etl.etl.scraper.factory_scraper import get_scraper_by_source
from review_etl.config.mongo_constants import DB_NAME
from review_etl.config.mongo_constants import COMPANY_COLLECTION
from review_etl.common.logger_utils import setup_logger
from review_etl.common.argparse_utils import parse_arguments


logger = logging.getLogger(setup_logger("append_company", "./logs"))


def main(source: str, company_ids: List[str] = None):
    # init mongo client
    load_dotenv(find_dotenv())
    scraper = get_scraper_by_source(source)
    with MongoClient(
        get_connect_string(os.environ.get("MONGODB_USR"), os.environ.get("MONGODB_PWD"))
    ) as client:
        db = client[DB_NAME]
        col = db[COMPANY_COLLECTION]
        for id in company_ids:
            try:
                company_info = scraper.get_company_info(id)
                res = col.update_one(
                    {"company_id": id}, {"$setOnInsert": company_info}, upsert=True
                )
                if res.upserted_id is None:
                    logger.info(f"Company: {id} is up-to-date. No upsert needed!")
                else:
                    logger.info(
                        f"Company: {id} has been upserted with {res.upserted_id}"
                    )
            except (DuplicateKeyError, Exception) as error:
                logger.error(traceback.format_exc())
    logger.info("Operation completed.")


if __name__ == "__main__":
    args = parse_arguments()
    main(args["source"], args["company_ids"])
