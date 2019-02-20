from config import *
from app_logger import *
import requests, csv

abuse_csv_response = requests.get(RANSOMWARE_TRACKER_URL)

if abuse_csv_response.status_code != 200:
    logger.error("Ransomware call returned a status code of {}".format(str(abuse_csv_response.status_code)))
else:
    logger.info("Successfully called Ransomware CSV")


