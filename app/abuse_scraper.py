import requests, csv, json, mongo_handler
from config import *
from app_logger import *
from sys import exit
from time import sleep

abuse_csv_response = requests.get(RANSOMWARE_TRACKER_URL)

if abuse_csv_response.status_code != 200:
    logger.error("Ransomware call returned a status code of {}".format(str(abuse_csv_response.status_code)))
    exit(1)
else:
    logger.info("Successfully retrieved Ransomware CSV")


# Firstseen (UTC),Threat,Malware,Host,URL,Status,Registrar,IP address(es),ASN(s),Country
#ransom_csv = csv.reader(abuse_csv_response.text.read().decode('ascii')) 
ransom_csv = csv.reader(abuse_csv_response.text.splitlines(), delimiter=',')
try:
    ransom_list = list(ransom_csv)
except Exception as e:
    logger.error("Unable to listify CSV :: {}".format(str(e)))

json_record = {}

for row in ransom_list:
    if len(row) < 2:
        pass
    else:
        firstSeen = row[0]
        threat = row[1]
        if threat == "Threat":
            # Skip the rows that tell us the CSV structure
            pass
        else:
            malware = row[2]
            host = row[3]
            url = row[4]
            status = row[5]
            registrar = row[6]
            IP = row[7]
            ASN = row[8]
            country = row[9]
            if IP == "":
                IP = "null"
            if url == "":
                url = "null"
            if host == "":
                host = "null"
            json_record = {"Threat": threat, "Malware": malware, "Host": host, "URL": url, "Status": status, \
                "Registrar": registrar, "IP": IP, "ASN": ASN, "Country": country, "FirstSeen": firstSeen}
            print(json.dumps(json_record))
            mongo_handler.loader(json.dumps(json_record))
            sleep(1)
            """
            if mongo_handler.loader(json_record):
                logger.info("Successful response from Mongo Handler")
            else:
                logger.error("Failure response from Mongo Handler")
            """