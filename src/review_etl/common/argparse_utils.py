import argparse


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(
        description="Ranking products for Adidas E-Com PLP pages"
    )
    parser.add_argument(
        "--source",
        choices=["app_store", "play_store"],
        help="Source of reviews for scraping. Defaults to play_store",
        default="play_store",
        type=str,
    )
    parser.add_argument(
        "--company_ids",
        help="Ids of the company in the source. For adidas, it is com.adidas.app",
        type=lambda company_ids: [
            company.strip() for company in company_ids.split(",") if company.strip()
        ],
        required=False,
    )
    parser.add_argument(
        "--lang",
        help="Language of the reviews to be scraped. Not required for all mains. 'en' or 'en, de, fr, tr' Defaults to 'en'",
        type=lambda langs: [lang.strip() for lang in langs.split(",") if lang.strip()],
        required=False,
        default=["en"],
    )
    parser.add_argument(
        "--unsafe-insertion",
        help="If provided, does unsafe insertion into DB, resulting in Duplicate Key Errors",
        action="store_true",
        dest="unsafe_insertion",
    )
    parser.add_argument(
        "--company-ids-from-db",
        help="If provided, scrape for company_ids in the database. company_id argument becomes irrelevant.",
        action="store_true",
        dest="company_ids_from_db",
    )

    args = parser.parse_args()
    return vars(args)
