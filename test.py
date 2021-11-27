import subprocess
import nmap
import socket
import sys
from datetime import datetime


# Gets list of hostnames and ips active on your network
# Problem: very slow
def getHosts():
    network_ip = f"{socket.gethostbyname(socket.gethostname())[:10]}0/24"

    print("Getting Hosts ...")
    nmScan = nmap.PortScanner()
    nmScan.scan(network_ip)
    host_list = nmScan.all_hosts()

    hosts = {}
    for host in host_list:
        hosts[nmScan[host].hostname()] = host

    print(f"Hosts: {hosts}")
    return hosts


# Creates and returns a device object
def getDeviceName():
    selection = input("Do you know the Name of the device? (y/n): ")
    if selection == "y":
        name = input("Device Name: ")
    else:
        hosts = getHosts()
        print("\nOptions:")
        for i, host in enumerate(hosts):
            print(f"{i+1} {host}")
        while True:
            choice = input(f"\nChoose host to listen to (1/{len(hosts)}): ")
            if choice.isdigit():
                if 1 <= int(choice) <= len(hosts):
                    name = list(hosts.keys())[int(choice) - 1]
                    confirm = input(f"Listen to {name}? (y/n): ")
                    if confirm == "y":
                        break
    return name


# Announces a message
def announce(name, home):
    past_verb = "arrived" if home else "left"
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = f"{name} has {past_verb} at {time}"
    print(message)


# Listens whether a device is or isn't on the network and announces it
def listen(name=False):
    if name is False:
        name = getDeviceName()

    print("Listening...")
    process = subprocess.Popen(["ping", name], stdout=subprocess.PIPE)
    home = False
    while True:
        line = process.stdout.readline()
        bytes = line.decode("utf-8").split()[0]

        if home:
            left = True
            for i in range(4):
                line = process.stdout.readline()
                bytes = line.decode("utf-8").split()[0]
                if bytes == "64":
                    left = False
            if left:
                home = False
                announce(name, home)

        elif bytes == "64" and not home:
            home = True
            announce(name, home)


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
    else:
        print("Usage: python listener.py <function> <args>")
