import requests, csv, json, mongo_handler
from config import RANSOMWARE_TRACKER_URL
from app_logger import logger
from sys import exit
from time import sleep
import watchguard_handler

abuse_csv_response = requests.get(RANSOMWARE_TRACKER_URL)

if abuse_csv_response.status_code != 200:
    logger.error("Ransomware call returned a status code of {}".format(str(abuse_csv_response.status_code)))
    exit(1)
else:
    logger.info("Successfully retrieved Ransomware CSV")


# Firstseen (UTC),Threat,Malware,Host,URL,Status,Registrar,IP address(es),ASN(s),Country
ransom_csv = csv.reader(abuse_csv_response.text.splitlines(), delimiter=',')

# Try to turn this CSV into a list
try:
    ransom_list = list(ransom_csv)
except Exception as e:
    logger.error("Unable to listify CSV :: {}".format(str(e)))

json_record = {}

record_count = 0

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
            # If this isn't an active threat, we can skip it
            if status == "offline":
                pass
            else:
                # If there isn't an IP, we can't do anything
                if IP == "":
                    pass

                else:

                    if url == "":
                        url = None
                    if host == "":
                        host = None
                    json_record = {"Threat": threat, "Malware": malware, "Host": host, "URL": url, "Status": status, \
                        "Registrar": registrar, "IP": IP, "ASN": ASN, "Country": country, "FirstSeen": firstSeen}
                    
                    # This msg is for pretty output when printing to console
                    
                    msg = """
                    Threat: {}
                    Malware: {}
                    Host: {}
                    Status: {}
                    IP: {}
                    Country: {}
                    URL: {}
                    """.format(str(threat), str(malware), str(host), str(status), str(IP), str(country), str(url))

                    # Check if we already have this IP in our database, which means we have it blocked
                    if not mongo_handler.check_existing_record(IP):
                        
                        # We're receiving a boolean depending on fail or success
                        if not watchguard_handler.add_alias_member(IP):
                            logger.error("Received failure from WatchGuard Handler")

                        else:
                            logger.info("Received success from WatchGuard Handler")
                            json_record['IpBlocked'] = True
                            mongo_handler.insert_malicious_record(json.dumps(json_record))

                    else:

                        pass