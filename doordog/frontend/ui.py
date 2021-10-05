""""""

import wx
import wx.lib.newevent
import wx.adv
from playsound import playsound
import doordog.events.read_tag as evt

class MyPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.st = wx.StaticText(self, label="Next ID will show here")
        font = self.st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.st.SetFont(font)

        img = wx.Image("doordog/assets/images/doordog_white.png", wx.BITMAP_TYPE_PNG)
        w = int(img.GetWidth()/4)
        h = int(img.GetHeight()/4)
        img = img.Scale(w,h)
        self.image = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        
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
    """"""
    #----------------------------------------------------------------------
    def __init__(self, pos):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Lan ETS - RFID Scanner", pos=pos)
        self.panel = MyPanel(self)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.reset, self.timer)
        self.Bind(evt.EVT_ON_READ_TAG_EVENT, self.on_read)
        # Enable full screen at event
        # self.ShowFullScreen(True)
        self.Show()
        # self.Maximize(True)

    def on_read(self, evt):
        self.set_text(evt.uid, evt.error)

    def set_text(self, text, error):
        if error:
            self.panel.SetBackgroundColour((255,0,0,255))
        else:
            self.panel.SetBackgroundColour((0,255,0,255))
        self.panel.st.SetLabel(text)
        self.panel.st.SetForegroundColour((0,0,0,255))
        self.timer.Start(1000, oneShot=wx.TIMER_ONE_SHOT)
        if error: 
            playsound('doordog/assets/audio/bad.mp3') 
        else:
            playsound('doordog/assets/audio/good_1.wav')

    def reset(self, event):
        self.panel.st.SetForegroundColour((255,255,255,255))
        self.panel.SetBackgroundColour((0,0,0,255))