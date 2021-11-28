import subprocess
import nmap
import socket
import sys
from datetime import datetime


# Returns a list of hostnames and ips active on your network
# FIXME very slow
def getHosts():
    network_ip = (
        # FIXME Is not accurate
        f"{socket.gethostbyname(socket.gethostname())[:10]}0/24"
    )
    print(network_ip)
    # TODO change nmap to scapy
    nmScan = nmap.PortScanner()
    nmScan.scan(network_ip)
    host_list = nmScan.all_hosts()

    hosts = {}
    for host in host_list:
        hosts[nmScan[host].hostname()] = host

    return hosts


# Returns an active device name or ip
def getDevice():
    print("Loading ...")
    hosts = getHosts()
    print("\nOptions:")
    for i, host in enumerate(hosts):
        print(f"{i+1} {host}")
    while True:
        choice = input(f"\nChoose host to listen to (1/{len(hosts)}): ")
        if choice.isdigit():
            if 1 <= int(choice) <= len(hosts):
                name, ip = list(hosts.items())[int(choice) - 1]
                break

    return (
        ip
        if input(f"list for 1: Name({name}) or 2: IP({ip})? (1/2): ") == "2"
        else name
    )


# Announces a message
def announce(device, home):
    past_verb = "arrived" if home else "left"
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = f"{device} has {past_verb} at {time}"
    print(message)


# Listens whether a device is or isn't on the network
def listen(device=False):
    if device is False:
        device = getDevice()

    print("Listening...")
    process = subprocess.Popen(["ping", device], stdout=subprocess.PIPE)
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
                announce(device, home)

        elif bytes == "64":
            home = True
            announce(device, home)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        listen()
    if len(sys.argv) == 2:
        device = sys.argv[1]
        listen(device)
    else:
        print("Usage: python listener.py <device name or ip>")
