import subprocess
import nmap
from decouple import config

IP_NETWORK = config("IP_NETWORK")
IP_DEVICE = config("IP_PHONE")
DEVICE_NAME = config("PHONE_NAME")


# Gets list of hostnames and ips active on your network
# Beware: very slow
def getHostNames():
    hosts = {}
    nmScan = nmap.PortScanner()
    nmScan.scan(IP_NETWORK)
    host_list = nmScan.all_hosts()
    for host in host_list:
        hosts[nmScan[host].hostname()] = host

    return hosts


# Listens whether a device is or isn't on the network and announces
def listenForRhys():
    process = subprocess.Popen(["ping", IP_DEVICE], stdout=subprocess.PIPE)
    home = True
    while True:
        line = process.stdout.readline()
        connected_ip = line.decode("utf-8").split()[3]
        if connected_ip == f"{IP_DEVICE}:" and not home:
            nmScan = nmap.PortScanner()
            nmScan.scan(IP_DEVICE)
            if nmScan[IP_DEVICE].hostname() == DEVICE_NAME:
                subprocess.Popen(["say", "Rhys is Home"])
                home = True
        elif home:
            check = 0
            for i in range(10):
                line = process.stdout.readline()
                connected_ip = line.decode("utf-8").split()[3]
                if connected_ip != f"{IP_DEVICE}:":
                    check += 1
            if check >= 8:
                subprocess.Popen(["say", "Rhys is not Home"])
                home = False


listenForRhys()
