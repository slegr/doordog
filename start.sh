#!/bin/bash

# Start it without sudo
# Wait for it to ask for password

# Get current user (not root)
user=$USER

# # Get list of devices with
# inputs=($(cat /proc/bus/input/devices | grep -4 Sycreader | grep H: | cut -f4 -d' '))

# for i in "${inputs[@]}"
# do
#    res=$(sudo chown $user "/dev/input/$i")
# done

# Change owner of devices used to $user, needs root permission
# Works well by itself on raspberry pi OS
sudo python3 ./doordog/utils/own_devices.py $user

# Start doordog
# This program cannot be started as sudo since some feature of wxpython won't work, e.g. the sound
python3 -m doordog