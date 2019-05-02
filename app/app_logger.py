import logging
from config import LOG_FILE, LOG_MODE

if LOG_MODE == "dev":
    logger = logging.getLogger('AbuseScraper')
    sh = logging.StreamHandler()
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(log_format)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
elif LOG_MODE == "prod":
    logger = logging.getLogger('AbuseScraper')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(LOG_FILE)
    handler.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(log_format)
    logger.addHandler(handler)
elif LOG_MODE == "none":
    logger = logging.getLogger('AbuseScraper')
    logger.propagate = False
else:
    logger = logging.getLogger('AbuseScraper')
    logger.setLevel(logging.INFO)
    logger.error("Invalid value for LOG_MODE in config.py")



