import logging
import yaml

logger = logging.getLogger("info")


def load_config(path):
    with open(path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.exception(exc)
