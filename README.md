# DoorDog 
![doordog_white](https://user-images.githubusercontent.com/17283078/135960499-7a949665-9fb9-41ea-9fa2-d746f8846987.png)
**[![Python package](https://github.com/slegr/doordog/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/slegr/doordog/actions/workflows/python-package.yml)**

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup and Installation](#setup-and-installation)
* [How to use](#how-to-use)
* [License](#license)

## General info
DoorDog is a boilerplate project for an event entrance/exit scan. It currently supports 13.56M RFID/NFC readers and tags.
It is built on python 3.8 and uses wxpython as GUI. In other words, DoorDog is a basic autonomous service waiting to scan new tags and post to a specific URL where the data will be stored and processed. The request response then determine audio and visual feedback to participants via the GUI.

## Requirements
- Debian like environment (Ubuntu, Raspbian, etc.)
- Python 3.8 (alredy installed in newer debian-like systems, like Ubuntu 20.04 or Raspberry Pi OS)
- wxPython (installed with installation scripts)

## Setup and Installation

First we need to install all required dependencies. There is an installation script for `Ubuntu 20.04` and for `Raspberry Pi OS 5.10` (previously called Raspbian)
```sh
git clone https://github.com/slegr/doordog
cd doordog
# Setup for ubuntu 20.04
./install/install_ubuntu_20.04.sh
# Setup for Raspbian
./install/install_raspbian.sh
# On Raspbian (Raspberry Pi OS), the installator add ./start.sh script to run on boot
# Make sure to reboot
sudo reboot
```

## How to use

1. Connect your usb RFID readers to the computer. Make sure they work by creating a text file and scanning an RFID/NFC card or chip. The ID writen on the card should print as text in the file.

2. Make a backup of `configs/config.yml` and edit the file with your own configs. Do not remove lines or parameter since some part of the program are dependent of it. Only edit it with your own preferences. To get your devices names, run the folling command and find the one(s) that correspond to your devices' specs.

    ```sh
    cat /proc/bus/input/devices
    ```

    For example, here is the device I use and the name I need to add in `configs/config.yml`

    ![result_devices](https://user-images.githubusercontent.com/17283078/135957548-e9f31f00-a518-48a2-a78f-c201b7261056.jpg)


3. Run the following script to launch the application. You will be asked for your password as sudoers, unless you are root by default (e.g. on Raspbian).
    
    ```sh
    ./start.sh
    ```


## Author
- slegr - https://github.com/slegr

## License
GNU GENERAL PUBLIC LICENSE
