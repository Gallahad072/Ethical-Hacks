import subprocess
import nmap
import socket
import sys
from datetime import datetime


class Device:
    def __init__(self, name, ip):
        self._name = name
        self._ip = ip

    def getName(self):
        return self._name

    def getIp(self):
        return self._ip

    def setIp(self, ip):
        self._ip = ip


# Returns a list of hostnames and ips active on your network
# Problem: very slow
def getHosts():
    network_ip = f"{socket.gethostbyname(socket.gethostname())[:10]}0/24"
    nmScan = nmap.PortScanner()
    nmScan.scan(network_ip)
    host_list = nmScan.all_hosts()

    hosts = {}
    for host in host_list:
        hosts[nmScan[host].hostname()] = host

    return hosts


# Creates and returns a device object
def getDevice():
    selection = input("Do you know the Name and IP of the device? (y/n): ")
    if selection == "y":
        name = input("Device Name: ")
        ip = input("Device IP: ")
    else:
        hosts = getHosts()
        print("\nOptions:")
        for i, host in enumerate(hosts):
            print(f"{i+1} {host}")
        while True:
            choice = input(f"\nChoose host to listen to (1/{len(hosts)}): ")
            if choice.isdigit():
                if 1 <= int(choice) <= len(hosts):
                    name, ip = list(hosts.items())[int(choice) - 1]
                    confirm = input(f"Listen to {name}? (y/n): ")
                    if confirm == "y":
                        break

    device = Device(name, ip)
    print(f"Device Name: {device.getName()}")
    print(f"Device IP: {device.getIp()}")
    return device


# Returns Device IP for the device once it's one the network
def getIpFromName(device_name):
    while True:
        hosts = getHosts()
        device_ip = hosts.get(device_name)
        if device_ip:
            print(f"Device IP: {device_ip}")
            return device_ip


# Returns Device name from the ip
def getNameFromIp(device_ip):
    print(f"Scanning for device name on IP port {device_ip} ...")
    nmScan = nmap.PortScanner()
    nmScan.scan(device_ip)
    device_name = nmScan[device_ip].hostname()
    print(f"Device name on {device_ip}: {device_name}")
    return device_name


# Announces a message
def announce(name, home):
    past_verb = "arrived" if home else "left"
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = f"{name} has {past_verb} at {time}"
    print(message)


# Listens whether a device is or isn't on the network and announces it
def listen(name=None, ip=None):
    if name:
        device = Device(name, ip) if name and ip else Device(name, getIpFromName(name))
    else:
        device = getDevice()

    print("Listening...")
    process = subprocess.Popen(["ping", device.getIp()], stdout=subprocess.PIPE)
    home = False
    while True:
        line = process.stdout.readline()
        bytes = line.decode("utf-8").split()[0]

        if home:
            left = True
            for i in range(3):
                line = process.stdout.readline()
                bytes = line.decode("utf-8").split()[0]
                if bytes == "64":
                    left = False
            if left:
                home = False
                announce(name, home)

        elif bytes == "64":
            if getNameFromIp(device.getIp()) == device.getName():
                home = True
                announce(name, home)
            else:
                # Sets new device ip if device name not on active ip
                device.setIp(getIpFromName(device.getName()))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        listen()
    if len(sys.argv) == 2:
        inpt = sys.argv[1]
        try:
            locals()[inpt]()
        except KeyError:
            print("\nError: Function not found\n")
    elif len(sys.argv) == 3:
        inpt = sys.argv[1]
        par1 = sys.argv[2]
        try:
            locals()[inpt](par1)
        except KeyError:
            print("\nError: Function not found\n")
    elif len(sys.argv) == 4:
        inpt = sys.argv[1]
        par1 = sys.argv[2]
        par2 = sys.argv[3]
        try:
            locals()[inpt](par1, par2)
        except KeyError:
            print("\nError: Function not found\n")
    else:
        print("Usage: python listener.py <function> <args>")
