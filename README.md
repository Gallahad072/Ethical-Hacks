# Network Listener

Welcome to a fun way to inflate one's ego, be paranoid, or track someone.

This [program](listener.py) will listen and announce when a certain device joins or leaves a network.

## Requirements

Install [nmap](https://nmap.org/download.html) onto your computer

Install python-nmap with pip:

`pip install python-nmap`

I am using python 3.9.8

## Functions

`listen(device)`

> This is the main function.
>
> Listens whether a device is or is not on the network and announces it.
>
> If a device is not passed in it will create a device.

`getHosts()`

> Returns a dictionairy of host names and ip addresses on the network.

`getDevice()`

> Returns a device selected by user from active devices on the network.

## Use

---

**Run the Main Program**

Type in the terminal:

`python listener.py`

---

**Run Specific Function**

Type in the terminal:

`python listener.py <device name or ip>`

---

**Run on a RaspberryPi**

_TO BE MADE_
