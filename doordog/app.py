""""""
import doordog.core.device_manager as dm
import doordog.frontend.ui as ui
import doordog.utils.configs as config
import wx

class DoorDog:
    """"""
    def __init__(self):
        self.configs = config.get_global_config()
        self.device_name = self.configs['devices']['names'][0]
        self.app = wx.App(False)
        self.device_manager = dm.DeviceManager(self.device_name)
        self.devices = self.device_manager.get_devices()
        self.frames = {}
        self.start()

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