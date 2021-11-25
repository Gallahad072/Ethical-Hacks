import subprocess
import nmap
from decouple import config


# Gets list of hostnames and ips active on your network
# Beware: very slow
def getHosts(network_ip):
    print("Getting Hosts:")
    hosts = {}
    nmScan = nmap.PortScanner()
    nmScan.scan(network_ip)
    host_list = nmScan.all_hosts()
    for host in host_list:
        hosts[nmScan[host].hostname()] = host
    print(f"Hosts: {hosts}")
    return hosts


# Returns Device IP for the device once it's one the network
def getDeviceIp(device_name):
    IP_NETWORK = config("IP_NETWORK")
    while True:
        hosts = getHosts(IP_NETWORK)
        device_ip = hosts.get(device_name)
        if device_ip:
            print(f"Device IP: {device_ip}")
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
                print("Rhys is Home")
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
                print("Rhys is not Home")
                subprocess.Popen(["say", "Rhys is not Home"])
                home = False


if __name__ == "__main__":
    listenForRhys()
