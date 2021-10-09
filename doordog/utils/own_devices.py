#!/usr/bin/env python3

import os
import pwd
import grp
import sys
import evdev
import yaml

def own_device(username):
    with open("./configs/config.yml") as f:
        configObj = yaml.load(f, Loader=yaml.FullLoader)
    configs = configObj['global-config']
    device_names = configs['devices']['names']
    all_devices = [evdev.InputDevice(dev) for dev in evdev.list_devices()]
    for device in all_devices:
        if device.name in device_names:
            uid = pwd.getpwnam(username).pw_uid
            gid = grp.getgrnam(username).gr_gid
            os.chown(device.path, uid, gid)
    return

if __name__ == '__main__':
    # Pass the user name to set as owner
    if len(sys.argv) <= 1:
        print("You need to pass in a UNIX username. Like 'python3 ... username'")
        exit(1)
    username = sys.argv[1]
    own_device(username)