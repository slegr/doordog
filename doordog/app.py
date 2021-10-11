#!/usr/bin/env python3

import doordog.core.device_manager as dm
import  doordog.frontend.ui_manager as ui
import doordog.utils.configs as config
import doordog.utils.logger as logger
import wx

class DoorDog:
    """
    Main class of the system representing the app entrance.
    The object should only be created once in the project and preferably in
    the __main__.py file. It creates the main components required for the system
    to work and start it self by starting the other components thread.
    """
    #---------------------------------------------------------------------
    def __init__(self):
        logger.info("Launching DoorDog...")
        self.ui_manager = ui.UIManager()
        self.device_manager = dm.DeviceManager(self.ui_manager.get_app_ref())
        self.ui_manager.create_frames(self.device_manager.get_device_names())
        self.start()

    #---------------------------------------------------------------------
    def start(self):
        self.device_manager.start()
        # Blocking loop
        self.ui_manager.start()
        self.device_manager.stop()
        self.device_manager.join()