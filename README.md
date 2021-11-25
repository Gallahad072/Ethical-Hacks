# Is Rhys Home?

Welcome to a fun way to inflate ones ego.

This [program](listener.py) will announce when a certain device comes off or on a network.

## Use

---

**Run the python file on your computer**

Type in the terminal:

`python listener.py`

---

**Run on a RaspberryPi**

_TO BE MADE_

---

## Setup

Create a '.env' file and fill it with:

```
IP_NETWORK = "192.168.x.0/24"
IP_PHONE = "192.168.x.xx"
PHONE_NAME = "Johns-IPhone.lan"
```

Replace the IP's with corresponding ones to your internet and device

Replace the name with then name of the device whose IP you entered

> If you don't know the name/ip of your device you can run `getHosts()`

## Import

On importing this as a module, one could either run:

`listener.listen()`

> Runs the main program

`listener.getHosts()`

> Returns a dictionairy of host names and ip addresses on the network import

`listener.getDeviceIp(device_name)`

> Returns the ip of a device once it's on the network
>
> Replace 'device_name' with the name of the device e.g. 'Johns-IPhone.lan'
