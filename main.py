import requests
import json
import socket
import os
import logging
import time

def getCurrentIp():
    # Try/catch incase of retrieve error
    try:
        parms = {'application': json}
        response = requests.get(url="http://ifconfig.co/json", params=parms)
        if response.status_code != 200:
            logger.error("Invalid response getting current Public IP")
            return "x.x.x.x"
        else:
            ipdata = response.json()
            logger.info("Get current Public IP: " + ipdata["ip"])
            return ipdata["ip"]
    except requests.exceptions.RequestException as e:
        logger.error("Exception raised getting current Public IP: " + e.strerror)
        return "x.x.x.x"

def getHostnameIp():
    # Try/catch incase of retrieve error
    try:
        addr = socket.gethostbyname(os.getenv("HOSTNAME"))
        logger.info("Get current Hostname IP: " + addr)
        return addr
    except socket.error as e:
        logger.error("Exception raised getting IP for " + os.getenv("HOSTNAME") + ": " + e.strerror)
        return "x.x.x.x"

def compareIp(addr1, addr2):
    if addr1 == addr2:
        logger.info("IP addresses match, nothing to update")
        return "skip"
    else:
        logger.info("IP adddress do not match, processing update")
        return "update"

def updateConnectIp(addr):
    uri = os.getenv("UPDATE_URL") + "?" + os.getenv("HOSTNAME") + "&myip=" + addr
    update = requests.post(url=uri, auth=(os.getenv("USERNAME"), os.getenv("PASSWORD")))
    logger.info("Update result: " + str(update.status_code))

def updateProcess():
    # Get public IP using retry logic(3), sleeping for seconds(5)
    i = 0
    while i < 3:
        pubIp = getCurrentIp()
        if pubIp == "x.x.x.x":
            i += 1
            time.sleep(5)
        else:
            i += 3
    
    # Get target IP using retry logic(3)
    i = 0
    while i < 3:
        conIp = getHostnameIp()
        if conIp == "x.x.x.x":
            i += 1
            time.sleep(5)
        else:
            i += 3


    # If either IP's cannot be determined log an error and stop update
    if pubIp == "x.x.x.x" or conIp == "x.x.x.x":
        logger.error("Error in getting IP's to evaluate, cancelling update")
    # Evaluate the IP's
    else:
        # If IP's match nothing to update
        if compareIp(pubIp, conIp) == "skip":
            pass
        # Else if IP's are different run the update
        else:
            try:
                updateConnectIp(pubIp)
            except:
                logger.error("Exception raised updating DDNS record: ")

if __name__ == '__main__':
    # create logger
    logger = logging.getLogger('DNS Updater (' + os.getenv("HOSTNAME") + ")")
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    while(True):
        updateProcess()
        time.sleep(300)





    
    
