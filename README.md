# DESCRIPTION

ETL to extract reviews from PlayStore

## Installation

### Prerequisites

Ensure that python3 is installed on your system.
Ensure that make is available on your system.
Ensure that curl is installed, as it's used for installing Poetry.

### Help

To view a list of all available tasks with descriptions, run:

```bash
make help
```

To install the project dependencies, run:

```bash
make install
```

Note that Makefile uses python3 to create the virtual environment and poetry installation. If you want to setup your virtual environment please assign your own python path to PYTHON env variable. This task will check if Poetry is installed, install it if necessary, and then install the project dependencies.

```bash
export PYTHON=<your own python path or alias>
make install
```

#### Running Tests

To run project tests, use:

```bash
make test
```

This task will execute the pytest command in the project’s virtual environment.

#### Cleaning The Project

To clean the project by removing the virtual environment and deleting the poetry.lock file, run:

### Manual Installation

1. Clone the repository.

2. Create a virtual environment with.

```bash
python3 -m venv .venv
source .venv/bin/activate
poetry config virtualenvs.in-project true
poetry install
```

## QUICKSTART

Our package is designed to scrape review from various sources such as PlayStore and App Store. Currently, we only have implementation for PlayStore.

To scrape all the reviews for a company you need to look-up the id of the company in the source (Play Store). For example Adidas has the id com.adidas.app in Play Store.
Assuming the virtual environment is active.

```bash
# scrape all reviews for Adidas, which are written in English
python -m review_etl.scripts.append_reviews --company_id com.adidas.app --lang en
# scrape all reviews for Adidas, with multiple languages
python -m review_etl.scripts.append_reviews --company_id com.adidas.app --lang en,fr,de,tr
# scrape all reviews for companies in db
python -m review_etl.scripts.append_reviews --company-ids-from-db --lang en,fr,de,tr
# Docker commands
docker run --env-file ./.env --platform linux/amd64 <imagename> <python command>
docker run --env-file ./.env  --platform linux/amd64 909552528127.dkr.ecr.eu-west-1.amazonaws.com/review_etl python -m review_etl.scripts.append_reviews --company_ids com.turknet.oim --lang en,de,fr,nl,tr

```

Note that unfortunately we cannot collect reviews per country. So, when we run the command above, this retrieves all English reviews written by people across different countries.
Also this will check whether com.adidas.app is in our company collection, if not, it appends this id to our company collection as well. That collection includes metadata at the aggregate level about the reviews.

When we run the command above for the second time, the program at first grabs the most latest reviewdate in the database and only scrape the reviews between that date and today's run date. So we don't need to scrape them all again and again

### APPENDING A COMPANY

To append a new company to our database

```bash
python -m review_etl.scripts.append_reviews --company_id com.adidas.app --lang en
```

### DB CREDENTIALS

Please include a **.env** file in your root with your user name **MONGODB_USR** and password
 **MONGODB_PWD**
