#!/usr/bin/env python3

from time import sleep
import wx
import wx.lib.newevent
import doordog.events.read_tag as evt
from doordog.frontend.frame import DDFrame
import doordog.utils.configs as config
import doordog.utils.logger as logger
import os
import bisect
# this line allows to hide annoying welcome message from pygame on loading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

DIVISIONS = {
    1: [1,1],
    2: [2,1],
    3: [3,1],
    4: [2,2],
    6: [3,2],
    8: [4,2],
    9: [3,3],
    12: [4,3],
    15: [5,3],
    16: [4,4]
}

class UIManager():
    """
    A class who is responsible for managing and maintaining the user interface
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        # Configs
        self.configs = config.get_global_config()['monitors']
        self.monitors_count = self.configs['count']
        # self.splitscreen = self.configs['count']
        self.rpm = self.configs['rpm']
        self.fullscreen = self.configs['fullscreen']
        self.reso_width = self.configs['default-resolution']['width']
        self.reso_height = self.configs['default-resolution']['height']
        self.app = wx.App(False)
        self.frames = {}
        self.refs = {}
        self.stopped = False
        self.app.Bind(evt.EVT_ON_READ_TAG_EVENT, self.on_read)
        self.app.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    #----------------------------------------------------------------------
    def get_app_ref(self):
        return self.app

    #----------------------------------------------------------------------
    def start(self):
        # Blocking loop
        self.app.MainLoop()
        while not self.stopped:
            sleep(1)

    #----------------------------------------------------------------------
    def on_key_down(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.stopped = True
            for key, frame in self.frames.items():
                frame.Close()
        else:
            event.Skip()

    #----------------------------------------------------------------------
    def create_frames(self, device_names):
        # Exit if no device passed
        if len(device_names) <= 0:
            logger.warning("No device detected :(")
            logger.warning("Please make sure to connect devices before launching DoorDog")
            self.stopped = True
            return
        # Set fullscreen to false if more devices than monitors
        if self.monitors_count < len(device_names):
            self.fullscreen = False

        layout = self.get_display_layout(len(device_names))

        # Create frames for all devices
        if self.monitors_count > 0:
            for idx, name in enumerate(device_names):
                temp_layout = layout[idx]
                self.frames[name] = DDFrame(temp_layout['x'], temp_layout['y'], temp_layout['width'], temp_layout['height'])

    #----------------------------------------------------------------------
    def get_display_layout(self, device_count):
        # More monitors than devices
        # if device_count < self.monitors_count: return 1
        # If Reader per Monitors is bigger then predefined layout, use last layout
        layout_keys = list(DIVISIONS.keys())
        if self.rpm > layout_keys[-1]:
            self.rpm = layout_keys[-1]
        layout = DIVISIONS.get(self.rpm)
        if layout == None:
            layout = DIVISIONS[min(x for x in layout_keys if x > self.rpm)]
        # Calculate dimensions
        frame_width = float(self.reso_width)/float(layout[0])
        frame_height = float(self.reso_height)/float(layout[1])
        dim_layout = []
        for y in range(layout[1]):
            for x in range(layout[0]):
                dim_layout.append({
                    'x': frame_width * x,
                    'y': frame_height * y,
                    'width': frame_width,
                    'height': frame_height,
                    })
        return dim_layout

    #----------------------------------------------------------------------
    def on_read(self, evt):
        frame = self.frames[evt.reader]
        if frame:
            frame.alert(evt.uid, evt.error)
