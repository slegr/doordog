""""""
import doordog.core.device_manager as dm
import doordog.frontend.ui as ui
import doordog.utils.configs as config
import wx

class DoorDog:
    """
    Main class of the system representing the app entrance.
    The object should only be created once in the project and preferably in
    the __main__.py file. t creates the main components required for the system
    to work and start it self by starting the other components thread.
    It also creates and assignes a frame (window) for each devices.
    """
    #---------------------------------------------------------------------
    def __init__(self):
        self.app = wx.App(False)
        self.device_manager = dm.DeviceManager()
        self.devices = self.device_manager.get_devices()
        self.frames = {}
        self.start()

    #---------------------------------------------------------------------
    def start(self):
        for dev in self.devices:
            # For multiple monitors, need to assign position for each window
            # frame = MyFrame(pos=wx.Point(1920,0))
            self.frames[dev.get_name()] = ui.MyFrame(pos=wx.Point(0,0))
            dev.set_frame_ref(self.frames[dev.get_name()])
        self.device_manager.start()
        self.app.MainLoop()
        self.device_manager.stop()
        self.device_manager.join()