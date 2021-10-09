""""""
import sys
import evdev
import requests
import json
from time import sleep
import threading
import wx
from datetime import datetime
import doordog.events.read_tag as evt
import doordog.utils.configs as config
import doordog.utils.logger as logger

class DeviceManager(threading.Thread):
    """
    A class who manages all the devices connected to the machine and finds the ones 
    with the names specified in config.yml
    The object returned is a Thread and needs to be started with the start() method.
    To stop the thread, simply call stop() on the object
    """
    #---------------------------------------------------------------------
    def __init__(self):
        threading.Thread.__init__(self)
        self.configs = config.get_global_config()
        self.setDaemon(1)
        self.lock = threading.Lock()
        self.stopped = False
        self.lock.acquire()
        self.devices = []
        # To change with for all possible names in config.yml
        self.device_name = self.configs['devices']['names'][0]
        self.update_devices()

    #---------------------------------------------------------------------
    def run(self):
        self.lock.release()
        while not self.stopped:
            self.update_devices()
            sleep(1)

    #---------------------------------------------------------------------
    def stop(self):
        self.stopped = True
        for device in self.devices:
            device.stop()

    #---------------------------------------------------------------------
    def get_devices(self):
        return self.devices

    #---------------------------------------------------------------------
    def device_in_listeners(self, device):
        for listener in self.devices:
            if listener.get_name() == device.phys:
                return True
        return False

    #---------------------------------------------------------------------
    def listener_in_devices(self, devices, listener):
        for device in devices:
            if device.phys == listener.get_name():
                return True
        return False
    
    #---------------------------------------------------------------------
    def update_devices(self):
        found_devices = [evdev.InputDevice(dev) for dev in evdev.list_devices()]
        # Add new connected devices
        for device in found_devices:
            if device.name == self.device_name and not self.device_in_listeners(device):
                self.add_device(device)
        # Remove missing devices listeners
        for device in self.devices:
            if not self.listener_in_devices(found_devices, device):
                self.devices.remove(device)

    #---------------------------------------------------------------------
    def add_device(self, device):
        self.devices.append(DeviceListener(device))

class DeviceListener:
    """
    A class who represent a listener on a specific reader device.
    The object should not be created on its own without management.
    It is prefered to let this responsability to the DeviceManager.
    """
    #---------------------------------------------------------------------
    def __init__(self, device):
        self.device = device
        self.configs = config.get_global_config()
        self.device.grab()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.stopped = False
        logger.info("New device connected : " + self.get_name())
        self.thread.start()

    #---------------------------------------------------------------------
    def stop(self):
        self.stopped = True
        self.device.ungrab()
        self.thread.join()

    #---------------------------------------------------------------------
    def set_frame_ref(self, frame_ref):
        self.frame_ref = frame_ref

    #---------------------------------------------------------------------
    def loop(self):
        uid = []
        try:
            while not self.stopped:
                event = self.device.read_one()
                if event:
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                        e_code = event.code - 1
                        if e_code >= 1 and e_code <= 10:
                            if e_code == 10:
                                uid.append(str(0))
                            else:
                                uid.append(str(e_code))
                            sys.stdout.flush()
                        elif e_code == 27: # enter minus one
                            self.code_scanned(uid)
                            uid = []
        except OSError:
            self.stop()
            del self

    #---------------------------------------------------------------------
    def get_name(self):
        return self.device.phys

    #---------------------------------------------------------------------
    def code_scanned(self, uid):
        formatedUID = uid=(''.join(uid))
        logger.info("Code Scanned: " + formatedUID)
        data = {
            'reader': self.get_name(),
            'uid': uid,
            'when': str(datetime.now())
        }
        # Check for blocked tags
        blocked_tags = self.configs['blocked-tags']
        if blocked_tags and formatedUID in blocked_tags:
            logger.warning("Tag " + formatedUID + " is blocked!")
            self.post_event(formatedUID, True)
        else:
            endpoint = self.configs['endpoints']['post-scan']
            response = requests.post(endpoint, data=data, timeout=3)
            logger.info("Response from " + endpoint + " - Status code = " + str(response.status_code))
            if response.status_code == 200 or response.status_code == 201:
                self.post_event(formatedUID, False)
            elif response.status_code == 404:
                print(response)
            else:
                print(response)
    #---------------------------------------------------------------------
    def post_event(self, uid, error):
        try:
            newEvt = evt.OnReadTagEvent(reader=self.get_name(), uid=uid, error=error)
            wx.PostEvent(self.frame_ref, newEvt)
        except RuntimeError:
            logger.error("Frame assigned to reader '" + self.get_name() + "' have been closed!")

    #---------------------------------------------------------------------
    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)