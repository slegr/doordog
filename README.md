# DoorDog
![doordog_white](https://user-images.githubusercontent.com/17283078/135960499-7a949665-9fb9-41ea-9fa2-d746f8846987.png)

DoorDog is a boilerplate project for an event entrance/exit scan. It currently supports 13.56M RFID/NFC readers and tags.
It is built on python 3.8 and uses wxpython as GUI.

## Requirements
- Debian like environment (Ubuntu, Raspbian, etc.)
- Python 3.8
- wxPython

## Setup and Installation

First we need to install all required dependencies. There is an installation script for `Ubuntu 20.04` and for `Raspberry Pi OS 5.10` (previously called Raspbian)
```sh
git clone https://github.com/slegr/doordog
cd doordog
# Setup for ubuntu 20.04
./setups/setup_ubuntu.sh
# Setup for Raspbian
./setups/setup_rpi.sh
```

## How to use

Make sure your USB Scanner devices are plugged in the machine and make sure they work well by going on a text file and scanning an RFID/NFC card or chip. The ID writen on the card should be printed in the file.

Edit the `configs/config.yml` with all your personnal configs. To get the name of your device, run the folling command and find the one(s) that correspond to your device's specs.
```sh
cat /proc/bus/input/devices
```
For example, here is the device I use and the name I need to add in `configs/config.yml`
![result_devices](https://user-images.githubusercontent.com/17283078/135957548-e9f31f00-a518-48a2-a78f-c201b7261056.jpg)


Run the following script to launch the application
```sh
./start.sh
```
