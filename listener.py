import socket
import nmap
import subprocess
import sys
from datetime import datetime


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


# Returns an active device name
def getDeviceName():
    print("Loading ...")
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


# Listens whether a device is or isn't on the network
def listen(name):
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
        listen(getDeviceName())
    if len(sys.argv) == 2:
        name = sys.argv[1]
        listen(name)
    else:
        print("Usage: python listener.py <device_name>")
