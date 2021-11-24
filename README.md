# Is Rhys Home?

Welcome to a fun way to inflate ones ego.

This [program](listener.py) will announce when a certain device comes off or on a network.

## Use

You can use it three ways:

---

**Run the python file on your computer**

Type in the terminal:

`python listener.py`

---

**Import and run modules**

For the main program import:

`from listener import main`

> Run this as a function 'main()'

To return a dictionairy of host names and ip addresses on the network import:

`from listener import getHosts`

> Run this as a function 'gethosts()'

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
