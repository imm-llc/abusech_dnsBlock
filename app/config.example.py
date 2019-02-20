MONGO_URL = 'mongodb://localhost:27017'
MONGO_DB = "abusech"
MONGO_COLLECTION = "ransomwareInfo"

"""
For authenticated mongo, use:
MONGO_URL = 'mongodb://userName:passWord@localhost:27017'
For remote authenticated mongo, use:
MONGO_URL = 'mongodb://userName:passWord@remoteHost:27017'

Change the port if needed
"""

RANSOMWARE_TRACKER_URL = "https://ransomwaretracker.abuse.ch/feeds/csv/"

# Available options are:
# dev
# prod
# none
# dev will print errors
# prod will log to file
LOG_MODE = "dev"
LOG_FILE = "/path/to/logfile"
