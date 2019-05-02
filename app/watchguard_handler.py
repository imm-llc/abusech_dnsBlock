from paramiko import client, AutoAddPolicy

import re

from config import WATCHGUARD_USER, WATCHGUARD_PASSWORD, WATCHGUARD_PORT, WATCHGUARD_IP, WATCHGUARD_ALIAS

from time import sleep

from app_logger import logger

"""
General idea of command sequence
Connect over SSH > configure > policy > alias MaliciousIP host-ip 83.217.11.193 > apply
"""


# Set up SSH client
client = client.SSHClient()

client.set_missing_host_key_policy(AutoAddPolicy())

def add_alias_member(ip_address):

    exp = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

    r = re.search(exp, ip_address)

    """
    Make sure we receive a valid IP address
    """
    if r is None:
        logger.error("Did not receive a valid IP address")
        return False

    # Connect to WatchGuard, set disable looking for keys
    # If you're using pubkey auth, you'll need to change some params here
    try:
        client.connect(WATCHGUARD_IP, port=WATCHGUARD_PORT, username=WATCHGUARD_USER, password=WATCHGUARD_PASSWORD, allow_agent=False, look_for_keys=False)
        logger.info("Connect to WatchGuard")
    except Exception as e:
        print("Error connecting to WatchGuard: {}".format(str(e)))
        return False

    # Invoke a shell that we can work with
    shell = client.invoke_shell()

    # Change to configure mode 
    shell.send("configure\n")
    sleep(2)

    # Change to policy mode
    shell.send("policy\n")
    sleep(2)

    # Add the IP to our alias containing blocked IPs
    shell.send("alias {} host-ip {} \n".format(WATCHGUARD_ALIAS, ip_address))
    sleep(2)
    # This response is a bytes-object
    response = shell.recv(2024)
    logger.info(f"Response from WatchGuard\n: {str(response)}")

    # Exit policy mode
    shell.send("exit\n")
    sleep(2)

    # Exit configure mode
    shell.send("exit\n")
    sleep(2)

    # Exit WatchGuard CLI
    shell.send("exit\n")
    sleep(2)

    # Close the shell we invoked
    shell.close()

    # Close the connection
    client.close()

    logger.info("Closed connection to WatchGuard")

    return True
