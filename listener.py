import subprocess
import nmap
from decouple import config


# Gets list of hostnames and ips active on your network
# Beware: very slow
def getHosts(network_ip):
    hosts = {}
    nmScan = nmap.PortScanner()
    nmScan.scan(network_ip)
    host_list = nmScan.all_hosts()
    for host in host_list:
        hosts[nmScan[host].hostname()] = host

    return hosts


def getDeviceIp(device_name):
    IP_NETWORK = config("IP_NETWORK")
    while True:
        print("here")
        hosts = getHosts(IP_NETWORK)
        print(hosts)
        device_ip = hosts.get(device_name)
        print(device_ip)
        if device_ip:
            print("returned")
            return device_ip


# Listens whether a device is or isn't on the network and announces
def listenForRhys():
    DEVICE_IP = config("IP_PHONE")
    DEVICE_NAME = config("PHONE_NAME")
    process = subprocess.Popen(["ping", DEVICE_IP], stdout=subprocess.PIPE)
    home = True
    while True:
        line = process.stdout.readline()
        connected_ip = line.decode("utf-8").split()[3]
        if connected_ip == f"{DEVICE_IP}:" and not home:
            nmScan = nmap.PortScanner()
            nmScan.scan(DEVICE_IP)
            if nmScan[DEVICE_IP].hostname() == DEVICE_NAME:
                subprocess.Popen(["say", "Rhys is Home"])
                home = True
            else:
                # Sets new device ip if device name not on active ip
                DEVICE_IP = getDeviceIp(DEVICE_NAME)
        elif home:
            check = 0
            for i in range(10):
                line = process.stdout.readline()
                connected_ip = line.decode("utf-8").split()[3]
                if connected_ip != f"{DEVICE_IP}:":
                    check += 1
            if check >= 8:
                subprocess.Popen(["say", "Rhys is not Home"])
                home = False


if __name__ == "__main__":
    listenForRhys()
