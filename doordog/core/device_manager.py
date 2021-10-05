""""""
import sys
import evdev
import requests
import json
from time import sleep
import threading
import wx
import doordog.events.read_tag as evt

########################################################################
class DeviceManager(threading.Thread):
    #---------------------------------------------------------------------
    def __init__(self, device_name):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.lock = threading.Lock()
        self.stopped = False
        self.lock.acquire()
        self.listening_devices = []
        self.device_name = device_name
        self.update_devices()

    #---------------------------------------------------------------------
    def run(self):
        self.lock.release()
        print(self.device_name)
        print("Ready to read...")
        while not self.stopped:
            self.update_devices()
            sleep(1)

    #---------------------------------------------------------------------
    def stop(self):
        self.stopped = True
        for device in self.listening_devices:
            device.stop()

    #---------------------------------------------------------------------
    def get_devices(self):
        return self.listening_devices

    #---------------------------------------------------------------------
    def device_in_listeners(self, device):
        for listener in self.listening_devices:
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
        for device in self.listening_devices:
            if not self.listener_in_devices(found_devices, device):
                self.listening_devices.remove(device)

    #---------------------------------------------------------------------
    def add_device(self, device):
        self.listening_devices.append(DeviceListener(device))

    #---------------------------------------------------------------------
    def print_devices(self):
        for device in self.listening_devices:
            print(device.get_name())

########################################################################
class DeviceListener:
    #---------------------------------------------------------------------
    def __init__(self, device):
        self.device = device
        self.device.grab()
        self.thread = threading.Thread(target=self.listening_loop, daemon=True)
        self.stopped = False
        self.thread.start()
        print(self.get_name(), self.device.path)

    def stop(self):
        self.stopped = True
        self.device.ungrab()
        self.thread.join()

    def set_frame_ref(self, frame_ref):
        self.frame_ref = frame_ref

    #---------------------------------------------------------------------
    def listening_loop(self):
        uid = []
        try:
            while not self.stopped:
                if event := self.device.read_one():
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                        e_code = event.code - 1
                        # print(event.code)
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
            del self

    #---------------------------------------------------------------------
    def get_name(self):
        return self.device.phys

    #---------------------------------------------------------------------
    def code_scanned(self, uid):
        formatedUID = uid=(''.join(uid)) 
        # response = requests.post("http://raspberrypi/api/scan/", data=parameters, timeout=3)
        response = requests.post("https://lanets.ca/health", timeout=3)
        # Notify.Notification.new("Hi").show()
        if response.status_code == 200 or response.status_code == 201:
            # self.jprint(response.json())
            error = False
            if formatedUID == "22211722":
                error = True
            newEvt = evt.OnReadTagEvent(reader=self.get_name(), uid=formatedUID, error=error)
            wx.PostEvent(self.frame_ref, newEvt)
        elif response.status_code == 404:
            print("Unknown tag or reader.")
        else:
            print(response)

    #---------------------------------------------------------------------
    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)