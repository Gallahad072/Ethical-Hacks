import subprocess
import nmap
from decouple import config

IP_NETWORK = config("IP_NETWORK")
IP_DEVICE = config("IP_DEVICE")
DEVICE_NAME = config("DEVICE_NAME")


def getHostNames():
    hosts = {}
    nmScan = nmap.PortScanner()
    nmScan.scan(IP_NETWORK)
    host_list = nmScan.all_hosts()
    for host in host_list:
        hosts[nmScan[host].hostname()] = host

    return hosts


def listenForRhys():
    proc = subprocess.Popen(["ping", IP_DEVICE], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        # the real code does filtering here
        connected_ip = line.decode("utf-8").split()[3]
        if connected_ip == f"{IP_DEVICE}:":
            nmScan = nmap.PortScanner()
            nmScan.scan(IP_DEVICE)
            if nmScan[IP_DEVICE].hostname() == DEVICE_NAME:
                subprocess.Popen(["say", "Rhys is Home"])
                break
