# Is Rhys Home?

Welcome to a fun way to inflate ones ego.

This [program](listener.py) will announce when a certain device comes off or on a network.

## Functions

`listen(name=None, ip=None)`

> This is the main function.
>
> Listens whether a device is or isn't on the network and announces it.
>
> If a Name and IP aren't passed in it will create a device..

`getHosts()`

> Returns a dictionairy of host names and ip addresses on the network import.

`getDevice()`

> Creates and returns a device object from user input.

`getIpFromName(device_name)`

> Returns the ip of a device from it's name once it's on the network.
>
> Replace 'device_name' with the name of the device e.g. 'Johns-IPhone'.

`getNameFromIp(device_ip)`

> Returns the name of a device from it's IP.
>
> Replace 'device_ip' with the IP of the device e.g. '192.168.0.3'.

## Use

---

**Run the Main Program**

Type in the terminal:

`python listener.py`

---

**Run Specific Function**

Type in the terminal:

`python listener.py <function> <args>`

---

**Run on a RaspberryPi**

_TO BE MADE_
