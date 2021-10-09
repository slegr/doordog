""""""

from typing import final
import wx
import wx.lib.newevent
import doordog.events.read_tag as evt
import doordog.utils.configs as config
import doordog.utils.logger as logger
import os
# this line allows to hide annoying welcome message from pygame on loading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

class MyPanel(wx.Panel):
    """
    A class who represent a Panel in a parent Window and a window only contains
    a single panel.
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.configs = config.get_global_config()
        self.st = wx.StaticText(self, label=self.configs['message'])
        font = self.st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.st.SetFont(font)
        # collect configs
        img_path = 'doordog/' + self.configs['background-image']['path']
        ratio = self.configs['background-image']['ratio']
        # Create Image
        img = wx.Image(img_path, wx.BITMAP_TYPE_PNG)
        ratio = 0.5 if ratio < 0 else ratio
        w = int(img.GetWidth() * ratio)
        h = int(img.GetHeight() * ratio)
        img = wx.Image(img.Scale(w,h))
        self.image = wx.StaticBitmap(self, wx.ID_ANY, img.ConvertToBitmap())
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddStretchSpacer()
        self.sizer.Add(self.st, 0, wx.CENTER)
        self.sizer.Add(self.image, 0, wx.CENTER)
        self.sizer.AddStretchSpacer()
        self.SetSizerAndFit(self.sizer)

        self.Bind(wx.EVT_KEY_DOWN, self.onKey)
        
    #----------------------------------------------------------------------
    def onKey(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.GetParent().Close()
        else:
            event.Skip()


class MyFrame(wx.Frame):
    """
    A class who represent a Frame (Window) which contains a single Panel.
    This class is also responsible for watching tag events and  editing its panel
    appearence.
    """
    #----------------------------------------------------------------------
    def __init__(self, pos):
        """Constructor"""
        self.configs = config.get_global_config()
        wx.Frame.__init__(self, None, title=self.configs['window-title'], pos=pos)
        self.panel = MyPanel(self)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.reset, self.timer)
        self.Bind(evt.EVT_ON_READ_TAG_EVENT, self.on_read)

        self.reset(None)
        
        if self.configs['monitors']['fullscreen']:    
            # Make sure to enable fullscreen at event
            self.ShowFullScreen(True)
        else:
            self.Show()
            # self.Maximize(True)

    #----------------------------------------------------------------------
    def on_read(self, evt):
        self.set_text(evt.uid, evt.error)

    #----------------------------------------------------------------------
    def set_text(self, text, error):
        bg_colour = wx.Colour()
        fg_colour = wx.Colour()
        if error:
            bg_colour.Set(self.configs['alerts']['error']['background-color'])
            fg_colour.Set(self.configs['alerts']['success']['foreground-color'])
        else:
            bg_colour.Set(self.configs['alerts']['success']['background-color'])
            fg_colour.Set(self.configs['alerts']['success']['foreground-color'])
        # Set new colours values on widgets
        self.panel.SetBackgroundColour(colour=bg_colour)
        self.panel.st.SetLabel(text)
        self.panel.st.SetForegroundColour(colour=fg_colour)
        # Set sound notif
        sound = 'doordog/' + self.configs['alerts']['success']['sound']
        if error:
            sound = 'doordog/' + self.configs['alerts']['error']['sound']

        # Starting the mixer
        mixer.init()
        # Launch timer to reset ui
        self.timer.Start(1000, oneShot=wx.TIMER_ONE_SHOT)
        try:
            # Loading the song
            mixer.music.load(sound)
            # Setting the volume
            mixer.music.set_volume(1)
            # Start playing the song in parallel
            mixer.music.play()
        except Exception as e:
            # print(e)
            logger.error(e)
        finally:
            pass

    #----------------------------------------------------------------------
    def reset(self, event):
        bg_colour = wx.Colour()
        fg_colour = wx.Colour()
        bg_colour.Set(self.configs['background-color'])
        fg_colour.Set(self.configs['foreground-color'])
        self.panel.st.SetForegroundColour(fg_colour)
        self.panel.SetBackgroundColour(bg_colour)