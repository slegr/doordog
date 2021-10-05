#!/bin/bash

# Start it without sudo
# Wait for it to ask for password

# Get current user (not root)
user=$USER

# Get list of device names entered in config.yml

# Get list of devices with
inputs=($(cat /proc/bus/input/devices | grep -4 Sycreader | grep H: | cut -f4 -d' '))

for i in "${inputs[@]}"
do
   res=$(sudo chown $user "/dev/input/$i")
done

python3 -m doordog