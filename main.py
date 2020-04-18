import requests
import json
import socket
import base64
import os
import logging
import time

def getPublicIp():
    parms = {'application': json}
    response = requests.get(url="http://ifconfig.co/json", params=parms)
    ipdata = response.json()
    logger.info("Get current Public IP: " + ipdata["ip"])
    return ipdata["ip"]

def getConnectIp():
    addr = socket.gethostbyname('connect.67uqr.net')
    logger.info("Get current Connect IP: " + addr)
    return addr

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

def processWrapper():
    pubIp = getPublicIp()
    conIp = getConnectIp()

    if compareIp(pubIp, conIp) == "skip":
        pass
    else:
        updateConnectIp(pubIp)

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

        processWrapper()

        time.sleep(300)





    
    
